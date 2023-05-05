use anyhow::Ok;

mod db;

const MemoryDB: &str = "sqlite::memory:";
const TestDB: &str = "sqlite:./test.db?mode=rwc";


#[tokio::main]
async fn main() -> anyhow::Result<()> {
    Ok(())
}
