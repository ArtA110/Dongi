from django.contrib.auth import get_user_model
from notification.tasks import send_email_with_template_task

User = get_user_model()

class SendEmail:
    def send_email_with_template(self, subject, template_file, context, ulid_list):
        users = User.objects.filter(id__in=ulid_list)
        
        user_context = self._extract_user_context(context, users)
        general_context = context.get('others', {})

        template_content = template_file.read().decode('utf-8')

        recipients = [user.email for user in users]
        send_email_with_template_task.delay(subject, template_content, user_context, general_context, recipients)

    def _extract_user_context(self, context, users):
        user_keys = context.get('user', [])
        if not user_keys:
            return {}

        result = []
        for user in users:
            user_data = {'email': user.email}
            for key in user_keys:
                if key == 'dongi_groups':
                    user_data[key] = [group.name for group in user.dongi_groups.all()]
                    continue
                user_data[key] = getattr(user, key, None)
            result.append(user_data)
        return result