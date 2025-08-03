import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from database import db
from datetime import datetime

# Initialize logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "7377637520:AAGiMzYQfSoVBDi257yE5GOlHTT5fadGX2k"
ADMIN_CHAT_ID = 7377637520

def generate_certificate(user_name, course_name, score):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Add certificate style
    styles.add(ParagraphStyle(
        name='CertificateTitle',
        fontSize=24,
        alignment=1,
        spaceAfter=20
    ))
    
    # Generate QR code
    cert_id = f"cert_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    qr = qrcode.make(f"https://t.me/IslamicTutorBot?start=verify_{cert_id}")
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    
    # Build PDF content
    elements = []
    elements.append(Paragraph("Certificate of Completion", styles['CertificateTitle']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"This is to certify that {user_name}", styles['Normal']))
    elements.append(Paragraph(f"has successfully completed the course", styles['Normal']))
    elements.append(Paragraph(f"{course_name}", styles['Heading2']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"with a score of {score}%", styles['Normal']))
    elements.append(Spacer(1, 30))
    elements.append(Image(qr_buffer, width=200, height=200))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer, cert_id

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.create_user(user.id, user.full_name)
    
    keyboard = [
        [InlineKeyboardButton("📚 Courses", callback_data="courses")],
        [InlineKeyboardButton("🎓 My Certificates", callback_data="certificates")],
        [InlineKeyboardButton("🏆 Tournaments", callback_data="tournaments")],
        [InlineKeyboardButton("🛠 CAD Tools", callback_data="cad_tools")]
    ]
    
    await update.message.reply_text(
        "🌟 Welcome to Islamic Tutoring Bot! 🌟",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Course system will be implemented soon!")

async def handle_certificates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Generate a sample certificate
    user = update.effective_user
    pdf_buffer, cert_id = generate_certificate(
        user.full_name,
        "Introduction to Islamic Studies",
        85
    )
    
    # Send certificate
    await context.bot.send_document(
        chat_id=user.id,
        document=InputFile(pdf_buffer, filename="certificate.pdf"),
        caption="🎉 Here's your sample certificate!"
    )

async def handle_cad_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("CAD tools will be implemented soon!")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_courses, pattern="^courses$"))
    application.add_handler(CallbackQueryHandler(handle_certificates, pattern="^certificates$"))
    application.add_handler(CallbackQueryHandler(handle_cad_tools, pattern="^cad_tools$"))
    
    application.run_polling()

if __name__ == '__main__':
    main()
