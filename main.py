# Imports
import os
import logging
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, CallbackContext, PicklePersistence,

)
from telegram.ext import ApplicationBuilder

from typing import Dict

# Bootstrap
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
reply_keyboard = [
    ["a company", "an Investor"],
    ["About Us"],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

INPUT_TYPE, TYPING_REPLY = range(0, 2)
C_NAME, C_WEBSITE, C_ABOUT = range(10, 13)
I_NAME, I_COMPANY, IC_WEBSITE, I_LINKEDIN = range(20, 24)


# METHODS
async def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Company", "Investor"]]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a company or an investor?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )

    return INPUT_TYPE


# async def done(update: Update, context:CallbackContext) -> int:
#     """Display the gathered info and end the conversation."""
#     user_data = context.user_data
#     if "choice" in user_data:
#         del user_data["choice"]
#
#     await update.message.reply_text(
#         f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#
#     user_data.clear()
#     return ConversationHandler.END
#
# async def regular_choice(update: Update, context:CallbackContext) -> int:
#     """Ask the user for info about the selected predefined choice."""
#     text = update.message.text
#     context.user_data["choice"] = text
#     await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")
#
#     return TYPING_REPLY
#
# def qa_choices(text):
#     text=text.lower()
#     # if text == "company name":
# async def qa_regular_choice(update: Update, context:CallbackContext) -> int:
#     """Ask the user for info about the selected predefined choice."""
#     text = update.message.text
#     context.user_data["choice"] = text
#
#     await update.message.reply_text(f"Please {text.lower()}? Yes, I would love to hear about that!")
#
#     return TYPING_REPLY
#
#
# async def custom_choice(update: Update, context:CallbackContext) -> int:
#     """Ask the user for a description of a custom category."""
#     await update.message.reply_text(
#         'Alright, please send me the category first, for example "Most impressive skill"'
#     )
#
#     return TYPING_CHOICE
#
def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


#
# async def received_information(update: Update, context:CallbackContext) -> int:
#     """Store info provided by user and ask for the next category."""
#     user_data = context.user_data
#     text = update.message.text
#     category = user_data["choice"]
#     user_data[category] = text
#     del user_data["choice"]
#
#     await update.message.reply_text(
#         "Neat! Just so you know, this is what you already told me:"
#         f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
#         " on something.",
#         reply_markup=markup,
#     )
#
#     return CHOOSING
async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def input_type(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    u_type = update.message.text.lower()
    msg = "Something went wrong. Please try again"
    if u_type == "company":
        msg = "I see! Please tell us your company name."
    if u_type == "investor":
        msg = "I see! Please us your name."
    logger.info("Input Type of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardRemove(),
    )

    context.user_data[u_type] = True
    if u_type == "company":
        return C_NAME
    if u_type == "investor":
        return I_NAME


# async def name_handler(update: Update, context: CallbackContext) -> int:
#     """Handles Name input"""
#     user = update.message.from_user
#
#     print(facts_to_str(context.user_data))
#     u_type=update.message.text.lower()
#     msg="Something went wrong. Please try again"
#     if u_type == "company":
#         msg=update.message.text+"I see! Please tell us your company name."
#     if u_type == "investor":
#         msg="I see! Please us your name."
#     logger.info("Input Type of %s: %s", user.first_name, update.message.text)
#     await update.message.reply_text(
#         msg,
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     if u_type == "company":
#         return C_NAME
#     if u_type == "investor":
#         return I_NAME

# async def received_information(update: Update, context: CallbackContext) -> int:
#     user_data = context.user_data
#     text = update.message.text
#     category = user_data["CATEGORY"]
#     user_data[category] = text
#     # del user_data["choice"]
#     print(context.user_data)
#
#     if "company" in user_data.keys():
#         return C_NAME
#     if "investor" in user_data.keys():
#         return I_NAME

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

async def company_handler(update: Update, context: CallbackContext) -> int:
    print(context.user_data)
    user_data = context.user_data
    text = update.message.text
    if not context.user_data['company']:
        await update.message.reply_text("Internal Error occurred! Please try again")
        print("Error in Company Handler")
        return ConversationHandler.END
    if 'C_NAME' not in user_data.keys():
        context.user_data['C_NAME'] = update.message.text
    else:
        user_data[user_data["CATEGORY"]] = update.message.text

    if 'C_WEBSITE' not in user_data.keys():
        await update.message.reply_text(f"Please provide us {text.lower()} website!")
        context.user_data['CATEGORY'] = 'C_WEBSITE'
        return C_NAME
    if 'C_ABOUT' not in user_data.keys():
        await update.message.reply_text(f"Can you tell us more about {text.lower()}!")
        context.user_data['CATEGORY'] = 'C_ABOUT'
        return C_NAME
    if {'C_NAME', 'C_WEBSITE', 'C_ABOUT'} <= user_data.keys():
        await update.message.reply_text(
            "Neat! Just so you know, this is what you already told me:"
            f"{facts_to_str(user_data)}"
            "information submitted successfully.",

        )
        #context.user_data={}
        return ConversationHandler.END

    print(user_data)


async def investor_handler(update: Update, context: CallbackContext) -> int:
    pass



def main() -> None:
    """Run the bot."""

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INPUT_TYPE: [MessageHandler(filters.Regex("^(Company|Investor)$"), input_type)],
            C_NAME: [MessageHandler(filters.TEXT, company_handler)],
            I_NAME: [MessageHandler(filters.TEXT, investor_handler)],
            # LOCATION: [
            #     MessageHandler(filters.LOCATION, location),
            #     CommandHandler("skip", skip_location),
            # ],
            # BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
            # TYPING_REPLY: [
            #     MessageHandler(
            #         filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
            #         received_information,
            #     )
            # ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling(stop_signals=None)


if __name__ == '__main__':
    main()
    print(TELEGRAM_BOT_TOKEN)
