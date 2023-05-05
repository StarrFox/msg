use serde::Serialize;
use chrono::Utc;

/// First second of 2023
const MSG_EPOCH: i64 = 1672531200;

#[derive(Serialize)]
pub(crate) struct SnowFlake {
    pub value: u64
}

#[derive(Clone)]
pub(crate) struct SnowFlakeGenerator {
    counter: u32,
}

impl SnowFlakeGenerator {
    pub fn new() -> Self {
        SnowFlakeGenerator {
            counter: 0,
        }
    }

    pub fn next(&mut self) -> SnowFlake {
        let timestamp = Utc::now().timestamp() - MSG_EPOCH;

        let mut id = (timestamp << 22) as u64;
        // TODO: replace with machine id
        id |= 1 << 12;
        id |= (self.counter & 0xFFF) as u64;

        self.counter += 1;

        // TODO: add some logic to make sure the next timestamp will be different
        if self.counter >= 0xFFF {
            self.counter = 0;
        }

        SnowFlake { value: id }
    }
}

