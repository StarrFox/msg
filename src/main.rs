use axum::{
    routing::post,
    http::StatusCode,
    Json,
    extract::State,
};
use serde::{Deserialize, Serialize};
use tokio::sync::RwLock;
use std::sync::Arc;

mod snowflake;

#[derive(Clone)]
struct AppState {
    snowflake_gen: snowflake::SnowFlakeGenerator,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let app_state = Arc::new(RwLock::new(AppState { snowflake_gen: snowflake::SnowFlakeGenerator::new() }));

    let router = axum::Router::new()
        .route("/messages", post(create_message))
        .with_state(app_state);

    let addr = std::net::SocketAddr::from(([127, 0, 0, 1], 3000));

    axum::Server::bind(&addr)
        .serve(router.into_make_service())
        .await?;

    Ok(())
}

async fn create_message(state: State<Arc<RwLock<AppState>>>, Json(payload): Json<CreateMessage>) -> (StatusCode, String) {
    let mut write_app_state = state.write().await;

    let id = write_app_state.snowflake_gen.next();
    
    let message = Message {
        id,
        content: payload.content,
    };

    // add message to channel and brodcast through events

    (StatusCode::CREATED, message.id.value.to_string())
}

#[derive(Deserialize)]
struct CreateMessage {
    content: String
}

#[derive(Serialize)]
struct Message {
    id: snowflake::SnowFlake,
    content: String,
}
