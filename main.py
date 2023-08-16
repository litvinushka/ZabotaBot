import telebot
from telebot import types

# Your bot token
bot_token = "6659595416:AAHOp734oEmMbXXO_r3k5N0w0zPZTDifz3g"
bot = telebot.TeleBot(bot_token)

# List of admin user IDs
admin_user_ids = [441740734]  # Replace with actual admin user IDs

# Dictionary to store user data
user_data = {}

# /start command handler
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item = types.KeyboardButton("Get a job")
    markup.add(item)
    bot.send_message(message.chat.id, "Hello! If you're looking for a job, press the button below.", reply_markup=markup)

# /getjob command handler
@bot.message_handler(func=lambda message: message.text == "Get a job")
def get_job(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id]:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        item = types.KeyboardButton("Submit Resume Again")
        markup.add(item)
        bot.send_message(message.chat.id, "You've already submitted your resume. Would you like to submit it again?", reply_markup=markup)
    else:
        job_form_url = "https://form.jotform.com/232215129751148"
        bot.send_message(message.chat.id, f"You can fill out the form to submit your resume here: {job_form_url}")
        user_data[user_id] = True

# Handler for the "Submit Resume Again" button
@bot.message_handler(func=lambda message: message.text == "Submit Resume Again")
def submit_resume_again(message):
    user_id = message.from_user.id
    user_data[user_id] = False
    job_form_url = "https://form.jotform.com/232215129751148"
    bot.send_message(message.chat.id, f"You can fill out the form to submit your resume again: {job_form_url}")
    
    # Notify all admin users about the user's resubmission
    user_info = f"User ID: {user_id}\nFirst Name: {message.from_user.first_name}\nLast Name: {message.from_user.last_name}\nUsername: @{message.from_user.username}"
    for admin_user_id in admin_user_ids:
        bot.send_message(admin_user_id, f"User submitted resume again:\n\n{user_info}")

# Start the bot
if __name__=="__main__":
    while True:
        try:
            bot.polling(non_stop=True)
        except Exception as e:
            print(e)
            continue