#!/usr/bin/env python3
"""Multi-agent server with routing.

Lab 2.9 Deliverable: Demonstrates AgentServer with multiple agents
and path-based routing for different specializations.
"""

from signalwire_agents import AgentServer, AgentBase, SwaigFunctionResult


# ============================================================
# General Agent - Main entry point
# ============================================================

class GeneralAgent(AgentBase):
    """General agent that can route to specialists."""

    def __init__(self):
        super().__init__(name="general-agent", route="/general")

        self.prompt_add_section(
            "Role",
            "You are the main receptionist. Help with general questions "
            "or route to sales or support specialists."
        )

        self.prompt_add_section(
            "Routing",
            bullets=[
                "For pricing/purchasing questions: route to sales",
                "For technical issues: route to support",
                "For general questions: answer directly"
            ]
        )

        self.add_language("English", "en-US", "rime.spore")
        self._setup_functions()

    def _setup_functions(self):
        @self.tool(description="Get company information")
        def get_company_info(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            return SwaigFunctionResult(
                "Welcome to TechCorp! We offer cloud software solutions. "
                "For sales, pricing, or support, I can connect you to a specialist."
            )

        @self.tool(description="Route to sales specialist")
        def route_to_sales(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            return (
                SwaigFunctionResult("Connecting you to our sales team.", post_process=True)
                .swml_transfer("/sales", "Goodbye!", final=True)
            )

        @self.tool(description="Route to support specialist")
        def route_to_support(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            return (
                SwaigFunctionResult("Connecting you to technical support.", post_process=True)
                .swml_transfer("/support", "Goodbye!", final=True)
            )


# ============================================================
# Sales Agent - Pricing and purchasing
# ============================================================

class SalesAgent(AgentBase):
    """Sales specialist agent."""

    PRICING = {
        "starter": {"price": 29, "users": 5, "features": "Basic"},
        "professional": {"price": 79, "users": 25, "features": "Advanced"},
        "enterprise": {"price": 199, "users": "Unlimited", "features": "Premium"}
    }

    def __init__(self):
        super().__init__(name="sales-agent", route="/sales")

        self.prompt_add_section(
            "Role",
            "You are a sales specialist. Help with pricing, plans, and purchasing."
        )

        self.prompt_add_section(
            "Available Plans",
            bullets=[
                f"{name.title()}: ${info['price']}/mo, {info['users']} users, {info['features']}"
                for name, info in self.PRICING.items()
            ]
        )

        self.add_language("English", "en-US", "rime.spore")
        self._setup_functions()

    def _setup_functions(self):
        @self.tool(description="Get all pricing plans")
        def get_pricing(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            plans = [
                f"{name.title()}: ${info['price']}/month for {info['users']} users"
                for name, info in self.PRICING.items()
            ]
            return SwaigFunctionResult("Our plans: " + "; ".join(plans))

        @self.tool(
            description="Get details for a specific plan",
            parameters={
                "type": "object",
                "properties": {
                    "plan": {
                        "type": "string",
                        "enum": ["starter", "professional", "enterprise"]
                    }
                },
                "required": ["plan"]
            }
        )
        def get_plan_details(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            plan = args.get("plan", "")
            info = self.PRICING.get(plan.lower())
            if not info:
                return SwaigFunctionResult("Plan not found.")
            return SwaigFunctionResult(
                f"{plan.title()} plan: ${info['price']}/month, "
                f"{info['users']} users, {info['features']} features."
            )

        @self.tool(
            description="Start a trial",
            parameters={
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "plan": {"type": "string"}
                },
                "required": ["email"]
            }
        )
        def start_trial(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            email = args.get("email", "")
            plan = args.get("plan", "professional")
            return (
                SwaigFunctionResult(
                    f"Great! I've started a 14-day trial of {plan} for {email}. "
                    "Check your inbox for login details."
                )
                .update_global_data({
                    "trial_email": email,
                    "trial_plan": plan,
                    "lead_captured": True
                })
            )


# ============================================================
# Support Agent - Technical assistance
# ============================================================

class SupportAgent(AgentBase):
    """Technical support agent."""

    def __init__(self):
        super().__init__(name="support-agent", route="/support")

        self.prompt_add_section(
            "Role",
            "You are technical support. Help with issues, troubleshooting, and account problems."
        )

        self.prompt_add_section(
            "Common Issues",
            bullets=[
                "Login problems: Reset password or check email",
                "Performance: Clear cache, check system requirements",
                "Integration: Verify API keys and permissions"
            ]
        )

        self.add_language("English", "en-US", "rime.spore")
        self._setup_functions()

    def _setup_functions(self):
        @self.tool(description="Get troubleshooting steps for login issues")
        def login_help(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            return SwaigFunctionResult(
                "For login issues: 1) Check your email is correct, "
                "2) Try password reset, 3) Clear browser cookies, "
                "4) Try incognito mode. Still stuck? I can create a ticket."
            )

        @self.tool(description="Get performance troubleshooting steps")
        def performance_help(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            return SwaigFunctionResult(
                "For performance issues: 1) Clear browser cache, "
                "2) Close other tabs, 3) Check internet connection, "
                "4) Try a different browser. Need more help?"
            )

        @self.tool(
            description="Create a support ticket",
            parameters={
                "type": "object",
                "properties": {
                    "issue": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"]
                    }
                },
                "required": ["issue"]
            }
        )
        def create_ticket(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            from datetime import datetime
            issue = args.get("issue", "")
            priority = args.get("priority", "medium")
            ticket_id = f"SUP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            return (
                SwaigFunctionResult(
                    f"Created ticket {ticket_id}. "
                    "We'll respond within 24 hours for standard issues."
                )
                .update_global_data({
                    "ticket_id": ticket_id,
                    "ticket_issue": issue,
                    "ticket_priority": priority
                })
            )

        @self.tool(description="Check system status")
        def system_status(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            return SwaigFunctionResult(
                "All systems operational. API: 99.9% uptime. "
                "No known issues. Last checked 5 minutes ago."
            )


# ============================================================
# Create and run server
# ============================================================

def create_server():
    """Create multi-agent server."""
    server = AgentServer(host="0.0.0.0", port=3000)

    # Register all agents
    server.register(GeneralAgent())
    server.register(SalesAgent())
    server.register(SupportAgent())

    return server


if __name__ == "__main__":
    server = create_server()
    server.run()
