from app import app, db, Message

with app.app_context():
    messages = Message.query.all()
    print(f"Found {len(messages)} messages:")
    for msg in messages:
        print(f"id={msg.id}, sender_id={msg.sender_id}, content={msg.content[:30]}, session_id={msg.session_id}, message_type={msg.message_type}, created_at={msg.created_at}")