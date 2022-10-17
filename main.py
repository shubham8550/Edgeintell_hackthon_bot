# Imports
import json
import os
import logging

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters, CallbackContext,

)
from telegram.ext import ApplicationBuilder

from typing import Dict

# Bootstrap
load_dotenv()
INVESTOR_APPSCRIPT_URL= os.getenv('INVESTOR_APPSCRIPT_URL')
COMPANY_APPSCRIPT_URL= os.getenv('COMPANY_APPSCRIPT_URL')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)


INPUT_TYPE, TYPING_REPLY = range(0, 2)
C_NAME, C_WEBSITE, C_ABOUT = range(10, 13)
I_NAME, I_COMPANY, IC_WEBSITE, I_LINKEDIN = range(20, 24)


# METHODS
async def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""

    reply_keyboard = [["Company", "Investor"]]

    await update.message.reply_text(
        "Hi! My name is " + context.bot.name + ". I will hold a conversation with you. "
                                               "Send /cancel to stop talking to me.\n\n"
                                               "Are you a company or an investor?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="company or investor?"
        ),
    )

    return INPUT_TYPE

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END


async def input_type(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    u_type = update.message.text.lower()
    msg = "Something went wrong. Please try again"
    if u_type == "company":
        msg = "I see! Please tell us your company name."
    if u_type == "investor":
        msg = "Hello! Please tell me your full name"
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


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    print("Test facts")

    facts = "Something is wrong! Please try again"
    if 'company' in user_data.keys():
        facts = f"\n" \
                f"Company - {user_data['C_NAME']}\n" \
                f"Website - {user_data['C_WEBSITE']}\n" \
                f"About   - {user_data['C_ABOUT']}\n"

    if 'investor' in user_data.keys():
        facts = f"\n" \
                f"Name - {user_data['I_NAME']}\n" \
                f"Invested in - {user_data['I_INVESTED_IN']}\n" \
                f"Website - {user_data['I_WEBSITE']}\n"
        if user_data['I_HAS_LINKEDIN'].lower() == 'yes':
            facts += f"LinkedIn   - {user_data['I_LINKEDIN']}\n"

    return facts


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
        await update.message.reply_text(f"Can you tell us more about {user_data['C_NAME']}!")
        context.user_data['CATEGORY'] = 'C_ABOUT'
        return C_NAME
    if {'C_NAME', 'C_WEBSITE', 'C_ABOUT'} <= user_data.keys():
        await update.message.reply_text(
            "Here is your Details-"
            f"{facts_to_str(user_data)}"
        )

        params = dict()
        params["action"] = "read"
        r = requests.get(COMPANY_APPSCRIPT_URL, params=params)
        if r.status_code == 200:
            print(r.content.decode('utf-8'))
            data = json.loads(r.content.decode('utf-8'))
            print(data)
            for i in data['records']:
                if i['Company_Name'].lower() == user_data['C_NAME'].lower():
                    await update.message.reply_text("The Data you want to add is already registered")
                    context.user_data.clear()
                    return ConversationHandler.END

            params = dict()
            params["action"] = "insert"
            params["name"] = user_data['C_NAME']
            params["website"] = user_data['C_WEBSITE']
            params["about"] = user_data['C_ABOUT']
            r = requests.get(COMPANY_APPSCRIPT_URL, params=params)
            print(r.status_code)

            await update.message.reply_text(
                f" Thank you {update.message.from_user.first_name}! your information successfully saved"
            )
        context.user_data.clear()

        return ConversationHandler.END

    print(user_data)


async def investor_handler(update: Update, context: CallbackContext) -> int:
    print(context.user_data)
    user_data = context.user_data
    text = update.message.text
    if not context.user_data['investor']:
        await update.message.reply_text("Internal Error occurred! Please try again")
        print("Error in Investor Handler")
        return ConversationHandler.END
    if 'I_NAME' not in user_data.keys():
        context.user_data['I_NAME'] = update.message.text
    else:
        user_data[user_data["CATEGORY"]] = update.message.text

    if 'I_INVESTED_IN' not in user_data.keys():
        await update.message.reply_text(
            f"Hey {user_data['I_NAME']}! Can you tell me the name of company in which you have invested?")
        context.user_data['CATEGORY'] = 'I_INVESTED_IN'
        return I_NAME
    if 'I_WEBSITE' not in user_data.keys():
        await update.message.reply_text(f"Nice!! Can provide us {user_data['I_INVESTED_IN']} Website?")
        context.user_data['CATEGORY'] = 'I_WEBSITE'
        return I_NAME
    if 'I_HAS_LINKEDIN' not in user_data.keys():
        await update.message.reply_text(f"{user_data['I_INVESTED_IN']} have linkedin account? Yes/No",
                                        reply_markup=ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True,
                                                                         input_field_placeholder="Yes/No"
                                                                         ))

        context.user_data['CATEGORY'] = 'I_HAS_LINKEDIN'
        return I_NAME
    if 'I_LINKEDIN' not in user_data.keys():
        if user_data['I_HAS_LINKEDIN'].lower() == "yes":
            await update.message.reply_text(f"Please provide {user_data['I_INVESTED_IN']} linkedin profile link",
                                            reply_markup=ReplyKeyboardRemove())
            context.user_data['CATEGORY'] = 'I_LINKEDIN'
            return I_NAME
        else:
            context.user_data['I_LINKEDIN'] = ""
            await update.message.reply_text(f"No problem! Thank you!",
                                            reply_markup=ReplyKeyboardRemove())

    if {'I_NAME', 'I_INVESTED_IN', 'I_WEBSITE', 'I_HAS_LINKEDIN', 'I_LINKEDIN'} <= user_data.keys():
        await update.message.reply_text(
            "Here is your Details- "
            f"{facts_to_str(user_data)}",
            reply_markup=ReplyKeyboardRemove()
        )
        params = dict()
        params["action"] = "read"
        r = requests.get(INVESTOR_APPSCRIPT_URL, params=params)
        if r.status_code == 200:
            print(r.content.decode('utf-8'))
            data = json.loads(r.content.decode('utf-8'))
            print(data)
            for i in data['records']:
                if i['Investors_Name'].lower() == user_data['I_NAME'].lower():
                    await update.message.reply_text("The Data you want to add is already registered")
                    context.user_data.clear()
                    return ConversationHandler.END

            params = dict()
            params["action"] = "insert"
            params["name"] = user_data['I_NAME']
            params["company"] = user_data['I_INVESTED_IN']
            params["website"] = user_data['I_WEBSITE']
            params["linkedin"] = user_data['I_LINKEDIN']
            r = requests.get(INVESTOR_APPSCRIPT_URL, params=params)
            print(r.status_code)

            await update.message.reply_text(
                f" Thank you {update.message.from_user.first_name}! your information successfully saved"
            )
        context.user_data.clear()
        return ConversationHandler.END

    print(user_data)


async def add_command_handler(update: Update, context: CallbackContext) -> int:
    if not context.args:
        await update.message.reply_text(
            "Invalid arguments.:"
            f"\n Syntax: /add company or /add investor"
        )
        return ConversationHandler.END
    if not (context.args[0].lower() == 'investor' or context.args[0].lower() == 'company'):
        await update.message.reply_text(
            "Invalid argument.:"
            f"\nSyntax: /add company or /add investor"
        )
        return ConversationHandler.END

    u_type = context.args[0].lower()
    user = update.message.from_user
    context.user_data[u_type] = True
    msg = "Something went wrong. Please try again"
    if u_type == "company":
        msg = "I see! Please tell us your company name."
    if u_type == "investor":
        msg = "Hello! Please tell me your full name"
    logger.info("Input Type of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        msg,
    )

    print(context.user_data)
    if u_type == "company":
        return C_NAME
    if u_type == "investor":
        return I_NAME


def main() -> None:
    """Run the bot."""

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("add", add_command_handler)],
        states={
            INPUT_TYPE: [MessageHandler(filters.Regex("^(Company|Investor)$"), input_type)],
            C_NAME: [MessageHandler(filters.TEXT, company_handler)],
            I_NAME: [MessageHandler(filters.TEXT, investor_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],

    )

    application.add_handler(conv_handler)
    application.run_polling(stop_signals=None)


if __name__ == '__main__':
    main()
