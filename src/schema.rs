// @generated automatically by Diesel CLI.

diesel::table! {
    messages (id) {
        id -> Nullable<Integer>,
        content -> Text,
    }
}
