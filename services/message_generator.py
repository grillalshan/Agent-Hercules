"""WhatsApp message template generator."""

from typing import Dict


class MessageGenerator:
    """Generates personalized WhatsApp messages for gym members."""

    def __init__(self, gym_name: str):
        """Initialize generator with gym name."""
        self.gym_name = gym_name
        self.templates = self._create_templates()

    def _create_templates(self) -> Dict[int, str]:
        """Create message templates for each cluster."""
        return {
            1: "Hi {name}, this is {gym_name}. Your membership {expiry_text}. Renew now to continue your fitness journey!",
            3: "Hi {name}, this is {gym_name}. Your membership will expire in 3 days on {date}. Renew soon to avoid interruption!",
            7: "Hi {name}, this is {gym_name}. Your membership will expire in 7 days on {date}. Don't miss out on your fitness goals!",
            30: "Hi {name}, this is {gym_name}. Your membership will expire in 30 days on {date}. Plan your renewal today!"
        }

    def generate_message(self, cluster: int, customer_name: str,
                        expiry_text: str, expiry_date: str,
                        days_remaining: int) -> str:
        """
        Generate personalized message for a customer.

        Args:
            cluster: Cluster number (1, 3, 7, or 30)
            customer_name: Customer's first name
            expiry_text: Human-readable expiry text (e.g., "expires today")
            expiry_date: Formatted expiry date (DD-MM-YYYY)
            days_remaining: Number of days remaining

        Returns:
            Personalized message string
        """
        template = self.templates.get(cluster, self.templates[1])

        # Extract first name only
        first_name = customer_name.split()[0] if customer_name else "Member"

        # Generate message
        message = template.format(
            name=first_name,
            gym_name=self.gym_name,
            expiry_text=expiry_text,
            date=expiry_date
        )

        return message

    def update_gym_name(self, gym_name: str):
        """Update gym name in templates."""
        self.gym_name = gym_name
        self.templates = self._create_templates()

    def get_template_preview(self, cluster: int) -> str:
        """Get template preview for a cluster."""
        template = self.templates.get(cluster, "")
        return template.format(
            name="[Customer Name]",
            gym_name=self.gym_name,
            expiry_text="[Expiry Text]",
            date="[DD-MM-YYYY]"
        )

    def customize_template(self, cluster: int, new_template: str):
        """
        Customize template for a specific cluster.

        Args:
            cluster: Cluster number
            new_template: New template string (must include {name}, {gym_name}, {expiry_text}, {date})
        """
        # Validate template has required placeholders
        required_placeholders = ['{name}', '{gym_name}']

        if cluster == 1:
            required_placeholders.append('{expiry_text}')
        else:
            required_placeholders.append('{date}')

        for placeholder in required_placeholders:
            if placeholder not in new_template:
                raise ValueError(f"Template must include {placeholder}")

        self.templates[cluster] = new_template
