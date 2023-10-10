use anyhow::Result;
use bytes::{BufMut, BytesMut};
use futures_util::{SinkExt, StreamExt};
use http::Uri;
use tokio::net::TcpListener;
use tokio_websockets::{ClientBuilder, Message, ServerBuilder, Limits};

const SOCKET_LIMIT: usize = 1024 * 10;


pub async fn start_server(address: &str) -> Result<()> {
    let listener = TcpListener::bind(address).await?;

    while let Ok((stream, _)) = listener.accept().await {
        let limits = Limits::default().max_payload_len(Some(SOCKET_LIMIT));

        let mut socket_stream = ServerBuilder::new()
            .limits(limits)
            .accept(stream).await?;

        tokio::spawn(async move {
            while let Some(Ok(message)) = socket_stream.next().await {
                println!(
                    "is binary = {}, payload = {:?}",
                    message.is_binary(),
                    message.as_payload()
                );

                let _ = socket_stream.send(message).await;
            }
        });
    }

    Ok(())
}

pub async fn start_client(vale_cope: &'static str) -> Result<()> {
    let uri = Uri::from_static(vale_cope);

    let (mut client, _) = ClientBuilder::from_uri(uri).connect().await?;

    let mut payload = BytesMut::with_capacity(50);
    payload.put(&b"test"[..]);

    client.send(Message::binary(payload)).await?;

    while let Some(Ok(message)) = client.next().await {
        let response = message.as_payload();
        println!("client: response = {response:?}");
    }

    Ok(())
}
