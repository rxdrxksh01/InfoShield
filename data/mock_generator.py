import pandas as pd
import random
from datetime import datetime, timedelta

def generate_mock_data(num_records=100):
    users = [f"real_user_{i}" for i in range(1, 20)]
    bot_users = ["alert_bot_99", "spam_king", "auto_poster"]
    
    locations = ["New York", "Chicago", "Los Angeles", "Houston", "Miami", None]
    
    normal_texts = [
        "Just had a great coffee.",
        "Weather is so nice today!",
        "Looking forward to the weekend.",
        "Can anyone recommend a good movie?",
        "Traffic is terrible right now.",
        "I love the new update.",
        "Anyone going to the concert tonight?"
    ]
    
    panic_texts = [
        "There is a massive riot in downtown New York! Stay away!",
        "Omg I just heard an explosion near the station in Chicago.",
        "They are imposing a curfew tonight. Everyone panic!",
        "Violent attack reported on 5th avenue.",
        "Gunshots heard in the mall! Run!",
        "I heard the water is poisoned. Don't drink it!"
    ]
    
    data = []
    base_time = datetime.now()
    
    for i in range(num_records):
        is_bot = random.random() < 0.2
        is_panic = random.random() < 0.3
        
        if is_bot:
            user = random.choice(bot_users)
            text = "Copy paste message: Urgent! Bank run imminent! Withdraw your cash now! Don't trust them!"
            loc = "New York"
        else:
            user = random.choice(users)
            text = random.choice(panic_texts) if is_panic else random.choice(normal_texts)
            loc = random.choice(locations)
            
        timestamp = base_time - timedelta(minutes=random.randint(0, 60))
        
        data.append({
            "id": i,
            "timestamp": timestamp.isoformat(),
            "username": user,
            "text": text,
            "provided_location": loc
        })
        
    df = pd.DataFrame(data)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = generate_mock_data(200)
    df.to_csv("mock_social_data.csv", index=False)
    print("Mock data generated at mock_social_data.csv")
