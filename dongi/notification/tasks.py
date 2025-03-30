import logging
from celery import shared_task
from django.core.mail import send_mail
from django.template import Template, Context
from django.utils.html import strip_tags
from django.conf import settings


logger = logging.getLogger(__name__)

@shared_task
def send_email_with_template_task(subject, template_content, user_context, general_context, recipients):
    logger.info(f'Received Email Task: {subject} to {recipients}')
    template = Template(template_content)

    for user_data in user_context:
        ctx = user_data.copy()  
        ctx.update(general_context)
        rendered_html_message = template.render(Context(ctx))
        plain_message = strip_tags(rendered_html_message)

        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [user_data['email']],
            html_message=rendered_html_message,
        )


    if not user_context:
        rendered_html_message = template.render(Context(general_context))
        plain_message = strip_tags(rendered_html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            recipients,
            html_message=rendered_html_message,
        )
    return f'Email Sent. {subject}, {recipients}'