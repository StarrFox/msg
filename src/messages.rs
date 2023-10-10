use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
#[serde(tag = "opcode")]
enum Message {
    /// echo this message back
    #[serde(rename = "0")]
    Echo {message: String}
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_serialize() {
        let message = Message::Echo { message: "test message".to_owned() };

        let as_json = serde_json::to_string_pretty(&message).unwrap();

        println!("{as_json}");
    }
}
