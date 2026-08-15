use axum::{
    extract::State,
    http::StatusCode,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    bridge_key: String,
}

#[derive(Deserialize)]
struct HealPayload {
    key: String,
    action: String,
    file_path: String,
    content: String,
}

#[derive(Serialize)]
struct HealResponse {
    status: String,
    path: String,
    engine: String,
}

#[tokio::main]
async fn main() {
    let state = Arc::new(AppState {
        bridge_key: "7600".to_string(),
    });

    let app = Router::new()
        .route("/health", get(|| async { "RUST_EDGE_ACTIVE" }))
        .route("/api/heal", post(heal_handler))
        .with_state(state);

    let addr = SocketAddr::from(([0, 0, 0, 0], 8080));
    println!("--- [RUST APEX ENGINE LISTENING ON {}] ---", addr);
    
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn heal_handler(
    State(state): State<Arc<AppState>>,
    Json(payload): Json<HealPayload>,
) -> (StatusCode, Json<HealResponse>) {
    if payload.key != state.bridge_key {
        return (
            StatusCode::FORBIDDEN,
            Json(HealResponse {
                status: "UNAUTHORIZED".to_string(),
                path: payload.file_path,
                engine: "Rust-WASM-v1".to_string(),
            }),
        );
    }

    // High-performance async disk write / injection
    tokio::fs::create_dir_all("cdn_assets").await.ok();
    let save_path = format!("cdn_assets/{}", payload.file_path);
    
    if let Some(parent) = std::path::Path::new(&save_path).parent() {
        tokio::fs::create_dir_all(parent).await.ok();
    }

    tokio::fs::write(&save_path, payload.content).await.ok();

    (
        StatusCode::OK,
        Json(HealResponse {
            status: "PERFECTED".to_string(),
            path: payload.file_path,
            engine: "Rust-Axum-Tokio".to_string(),
        }),
    )
}
