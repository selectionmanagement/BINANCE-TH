import random
import time
import pytz
from datetime import datetime

# Function to calculate trade size in BTC
def calculate_trade_size(fix_asset_1, current_btc_value, ask_price):
    ask_price = float(ask_price)  # Ensure ask price is a float
    size = (fix_asset_1 - current_btc_value) / ask_price  # Calculate trade size in BTC
    return size  # This can be positive or negative depending on buy/sell

# Function to execute trade logic
def execute_trade_logic(fix_asset_1, current_btc_value, ask_price, fix_percent=0.01):
    # Get current time in Bangkok timezone
    bangkok_tz = pytz.timezone('Asia/Bangkok')
    current_time = datetime.now(bangkok_tz).strftime('%Y-%m-%d %H:%M:%S')

    # Print the current time in Bangkok timezone
    print(f"Current Time (Bangkok): {current_time}")
    
    # Calculate thresholds for rebalancing (1% deviation)
    upper_threshold = fix_asset_1 + (fix_asset_1 * fix_percent)
    lower_threshold = fix_asset_1 - (fix_asset_1 * fix_percent)
    
    # Calculate the trade size (how much BTC to buy or sell)
    btc_size = calculate_trade_size(fix_asset_1, current_btc_value, ask_price)
    formatted_btc_size = f"{btc_size:.6f}"  # Format size to 6 decimal places
    equivalent_usd = abs(btc_size * ask_price)  # Calculate the equivalent USD value

    # Print details for monitoring
    print(f"BTC Price: {ask_price}")
    print(f"Fixed BTC Value (Target): {fix_asset_1}")  # This should always remain constant (e.g., 5000)
    print(f"Current BTC Value: {current_btc_value}")
    
    if current_btc_value > upper_threshold:
        print(f"Size to Sell: {formatted_btc_size} BTC")
        print(f"Equivalent USD: ${equivalent_usd:.2f}")
        print("Action: SELL order should be placed.")
    
    elif current_btc_value < lower_threshold:
        print(f"Size to Buy: {formatted_btc_size} BTC")
        print(f"Equivalent USD: ${equivalent_usd:.2f}")
        print("Action: BUY order should be placed.")
    
    else:
        print("BTC value is within the threshold limits. No trade executed.")
    print("\n" + "-"*40 + "\n")  # For better readability in the output

# Initial setup
capital = 10000  # Capital in USDT
fix_asset = 5000  # Starting fixed value for BTC (the target fixed value that does NOT change)
initial_ask_price = 45000  # Assume the price of BTC when starting
btc_size = fix_asset / initial_ask_price  # Amount of BTC bought in the first trade

print(f"Starting the trade: Bought BTC worth ${fix_asset} at ${initial_ask_price} per BTC")
print(f"BTC size: {btc_size:.6f} BTC\n")

# Time cycle settings (dynamic time intervals)
multi = 60  # base multiplier in seconds
time_cycles = [1, 1, 2, 3, 5, 8, 1, 1, 2, 3, 5, 8, 1, 1, 2]  # dynamic time intervals

# Run a continuous simulation with a while loop and dynamic time intervals
cycle_index = 0  # To track the current cycle

while True:  # Infinite loop
    # Generate a random ask_price between 40,000 and 50,000 for simulation
    ask_price = random.uniform(40000, 50000)
    
    # Calculate the current value of BTC holdings based on the new ask price
    current_btc_value = btc_size * ask_price  # Value of current BTC holdings
    
    # Execute trade logic with the random ask_price, while keeping fix_asset constant at 5000
    execute_trade_logic(fix_asset, current_btc_value, ask_price)
    
    # Determine the sleep time based on the current time cycle
    sleep_time = time_cycles[cycle_index] * multi
    print(f"Waiting for {sleep_time} seconds before the next check.\n")
    
    # Wait for the calculated time before the next iteration
    time.sleep(sleep_time)
    
    # Move to the next time cycle, loop back to the beginning of the list if needed
    cycle_index = (cycle_index + 1) % len(time_cycles)  # Cycle through time_cycles indefinitely
