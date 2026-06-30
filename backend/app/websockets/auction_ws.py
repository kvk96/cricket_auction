"""WebSocket handler for live auction updates."""
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from typing import Dict, List
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

router = APIRouter()

# Store active auction connections
active_auctions: Dict[int, List[WebSocket]] = {}


@router.websocket("/ws/auction/{auction_id}")
async def websocket_auction_endpoint(websocket: WebSocket, auction_id: int):
    """WebSocket endpoint for live auction updates."""
    await websocket.accept()
    
    # Initialize auction if not exists
    if auction_id not in active_auctions:
        active_auctions[auction_id] = []
    
    active_auctions[auction_id].append(websocket)
    logger.info(f"Client connected to auction {auction_id}")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Broadcast to all clients in this auction
            await broadcast_to_auction(
                auction_id,
                {
                    "type": message.get("type"),
                    "data": message.get("data"),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )
    except WebSocketDisconnect:
        active_auctions[auction_id].remove(websocket)
        logger.info(f"Client disconnected from auction {auction_id}")
        if not active_auctions[auction_id]:
            del active_auctions[auction_id]
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.close(code=status.WS_1011_SERVER_ERROR)
        except:
            pass


async def broadcast_to_auction(auction_id: int, message: dict):
    """Broadcast a message to all clients connected to an auction."""
    if auction_id not in active_auctions:
        return
    
    disconnected = []
    for websocket in active_auctions[auction_id]:
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            disconnected.append(websocket)
    
    # Remove disconnected clients
    for websocket in disconnected:
        active_auctions[auction_id].remove(websocket)


async def send_auction_update(
    auction_id: int,
    update_type: str,
    data: dict,
):
    """Send an auction update to all connected clients."""
    await broadcast_to_auction(
        auction_id,
        {
            "type": update_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
