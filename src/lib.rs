use chrono::{DateTime, Utc};

/// Snowflake
struct Snowflake {
    /// Internal value
    value: u64,
}

impl Snowflake {
    pub fn new(timestamp: u32, machine_id: u32, counter: u32) -> Self {
        let mut value: u64 = (timestamp as u64) << 22;
        value &= (machine_id as u64) << 12;
        value &= counter as u64;

        Snowflake{value}
    }

    pub fn get_timestamp(&self) -> DateTime<Utc> {
        todo!()
    }

    pub fn get_machine_id(&self) {
        todo!()
    }

    pub fn get_counter(&self) {
        todo!()
    }
}

#[cfg(test)]
mod test {
    use crate::Snowflake;

    #[test]
    fn test_timestamp() {
        let now = chrono::Utc::now();

        let snow = Snowflake::new(now.timestamp() as u32, 1, 1);

        assert!(snow.get_timestamp() == now.timestamp())
    }
}
