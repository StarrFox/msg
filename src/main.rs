use anyhow::Result;

mod snowflake;
mod websocket;

const ADDRESS: &str = "127.0.0.1:9000";
// rust trolling
const CLIENT_ADDRESS: &str = "ws://127.0.0.1:9000";

#[tokio::main]
async fn main() -> Result<()> {
    let _ = tokio::join!(
        websocket::start_server(ADDRESS),
        websocket::start_client(CLIENT_ADDRESS)
    );

    Ok(())
}
