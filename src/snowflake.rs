use chrono::{DateTime, Utc};

/// First second of 2023
const MSGEPOCH: u64 = 1672531200;

struct SnowFlake {
    value: u64,
}

impl SnowFlake {
    pub fn get_timestamp(&self) -> u64 {
        (self.value >> 22) + MSGEPOCH
    }

    pub fn get_machine_id(&self) -> u32 {
        // machine id is 10 bits long
        ((self.value >> 12) & 0b1111111111) as u32
    }

    pub fn get_counter(&self) -> u32 {
        (self.value & 0b111111111111) as u32
    }

    pub fn when(&self) -> Option<DateTime<Utc>> {
        DateTime::from_timestamp(self.get_timestamp() as i64, 0)
    }
}

struct SnowFlakeGenerator {
    machine_id: u32,
    counter: u32,
    rollover_timestamp: i64,
}

impl SnowFlakeGenerator {
    fn new(machine_id: u32) -> SnowFlakeGenerator {
        SnowFlakeGenerator {
            machine_id: machine_id,
            counter: 0,
            rollover_timestamp: 0,
        }
    }

    fn next(&mut self) -> SnowFlake {
        let mut timestamp = Utc::now().timestamp() - MSGEPOCH as i64;

        if self.counter == 0 {
            while timestamp == self.rollover_timestamp {
                timestamp = Utc::now().timestamp() - MSGEPOCH as i64;
            }
        }

        let mut snowflake_value = (timestamp << 22) as u64;

        snowflake_value |= (self.machine_id << 12) as u64;
        snowflake_value |= (self.counter & &0b111111111111) as u64;

        self.counter += 1;

        if self.counter >= 0b111111111111 {
            self.rollover_timestamp = timestamp;
            self.counter = 0;
        }

        SnowFlake {
            value: snowflake_value,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_epoch() {
        let msg_datetime = DateTime::from_timestamp(MSGEPOCH as i64, 0).unwrap();
        assert!(msg_datetime.to_string() == "2023-01-01 00:00:00 UTC");
    }

    #[test]
    fn test_properties() {
        let mut generator = SnowFlakeGenerator::new(123);

        let flake = generator.next();

        assert!(flake.get_counter() == 0);
        assert!(flake.get_machine_id() == 123);
    }

    #[test]
    fn test_rollover() {
        let mut generator = SnowFlakeGenerator::new(123);

        for _ in 0..0b111111111111 {
            let _ = generator.next();
        }

        assert!(generator.counter == 0);

        let mut last: SnowFlake = SnowFlake { value: 0 };

        for _ in 0..0b111111111111 {
            last = generator.next();
        }

        let rollover = generator.next();

        assert!(rollover.get_timestamp() != last.get_timestamp());
    }
}
