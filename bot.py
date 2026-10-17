import discord
from discord.ext import commands
from discord.ui import Select, View

# ==========================================================
# CONFIGURATION & FORM LINKS
# ==========================================================
FIREFIGHTER_FORM_LINK = "https://forms.gle/5kXSQPsZhi4KCtv46"
EMS_FORM_LINK = "https://forms.gle/NszN6Hq84Np2Qvu6A"
FTO_FORM_LINK = "https://forms.gle/ejyWmcCo2zzR35SV7"

# Setup Bot Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ==========================================================
# DROPDOWN SELECT MENU
# ==========================================================
class ApplicationDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Apply for Firefighter",
                value="firefighter",
                description="Submit an application for Fire Suppression operations.",
                emoji="🚒"
            ),
            discord.SelectOption(
                label="Apply for EMS (EMT)",
                value="ems",
                description="Submit an application for Emergency Medical Services.",
                emoji="🚑"
            ),
            discord.SelectOption(
                label="Apply for FTO Program",
                value="fto",
                description="Requires Firefighter III or Advanced EMT role.",
                emoji="📋"
            )
        ]
        super().__init__(
            placeholder="Select an application category...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="fdny_app_dropdown_select"
        )

    async def callback(self, interaction: discord.Interaction):
        selection = self.values[0]

        # 1. FIREFIGHTER SELECTION
        if selection == "firefighter":
            embed = discord.Embed(
                title="🚒 NEW YORK CITY FIRE DEPARTMENT — FIREFIGHTER RECRUITMENT",
                description=(
                    "The **FDNY Recruitment Bureau** is officially accepting applications for motivated individuals looking to serve the city of New York! If you have what it takes to perform structural firefighting, search and rescue, and vehicle extrications, apply today to earn your bunker gear.\n\n"
                    "### 📋 **OPEN DIVISIONS**\n"
                    "- 🚒 **Fire Suppression Division** — Engine & Ladder operations\n\n"
                    "### 📌 **REQUIREMENTS**\n"
                    "- Must be a member of the server in good standing.\n"
                    "- Must have a clean disciplinary record (no recent bans or severe warnings).\n"
                    "- Working microphone and clear communication skills.\n"
                    "- Basic understanding of department protocols and roleplay rules.\n\n"
                    "### 📩 **HOW TO APPLY**\n"
                    "1. Click the application link below to open the form:\n"
                    f"👉 **<{FIREFIGHTER_FORM_LINK}>**\n"
                    "2. Fill out the application form completely and accurately.\n"
                    "3. Submit your response and wait for recruitment staff review!\n\n"
                    "*If approved, you will receive a direct notification and your entry-level department role will be assigned automatically.*"
                ),
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        # 2. EMS SELECTION
        elif selection == "ems":
            embed = discord.Embed(
                title="🚑 NEW YORK CITY FIRE DEPARTMENT — EMS RECRUITMENT",
                description=(
                    "The **FDNY Recruitment Bureau** is officially accepting applications for dedicated individuals looking to provide life-saving care across New York City! If you have what it takes to provide basic life support, emergency patient care, and rapid medical response, apply today to earn your uniform.\n\n"
                    "### 📋 **OPEN DIVISIONS**\n"
                    "- 🚑 **Emergency Medical Services (EMS)** — Basic Life Support (EMT) Operations\n\n"
                    "### 📌 **REQUIREMENTS**\n"
                    "- Must be a member of the server in good standing.\n"
                    "- Must have a clean disciplinary record (no recent bans or severe warnings).\n"
                    "- Working microphone and clear communication skills.\n"
                    "- Basic understanding of medical roleplay guidelines and department protocols.\n\n"
                    "### 📩 **HOW TO APPLY**\n"
                    "1. Click the application link below to open the form:\n"
                    f"👉 **<{EMS_FORM_LINK}>**\n"
                    "2. Fill out the application form completely and accurately.\n"
                    "3. Submit your response and wait for recruitment staff review!\n\n"
                    "*If approved, you will receive a direct notification and your entry-level department role will be assigned automatically.*"
                ),
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        # 3. FTO SELECTION (WITH ROLE CHECK)
        elif selection == "fto":
            required_roles = ["Firefighter III", "Advanced EMT"]
            
            # Check if user has either Firefighter III or Advanced EMT role
            user_role_names = [role.name for role in interaction.user.roles]
            has_permission = any(role in user_role_names for role in required_roles)

            if has_permission:
                embed = discord.Embed(
                    title="📋 NEW YORK CITY FIRE DEPARTMENT — FTO RECRUITMENT",
                    description=(
                        "The **FDNY Recruitment Bureau** is officially accepting applications for experienced members looking to join the Field Training Officer program! Help train and guide our probationary firefighters and medics.\n\n"
                        "### 📋 **OPEN DIVISIONS**\n"
                        "- 📋 **Field Training Officer Program** — Trainee supervision & evaluation\n\n"
                        "### 📌 **REQUIREMENTS**\n"
                        "- Must be a member of the server in good standing.\n"
                        "- Must hold either **Firefighter III** or **Advanced EMT** rank.\n"
                        "- Excellent leadership and communication skills.\n\n"
                        "### 📩 **HOW TO APPLY**\n"
                        "1. Click the application link below to open the form:\n"
                        f"👉 **<{FTO_FORM_LINK}>**\n"
                        "2. Fill out the application form completely and accurately.\n"
                        "3. Submit your response and wait for recruitment staff review!\n\n"
                        "*If approved, you will receive a direct notification and your entry-level department role will be assigned automatically.*"
                    ),
                    color=discord.Color.gold()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(
                    "❌ **Access Denied**\n"
                    "You must hold either the **Firefighter III** or **Advanced EMT** role to apply for the Field Training Officer (FTO) program.",
                    ephemeral=True
                )


# ==========================================================
# VIEW WRAPPER FOR DROPDOWN
# ==========================================================
class ApplicationPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)  # Keeps view active permanently across bot restarts
        self.add_item(ApplicationDropdown())


# ==========================================================
# BOT EVENTS & COMMANDS
# ==========================================================
@bot.event
async def on_ready():
    bot.add_view(ApplicationPanelView())
    print(f"Logged in as {bot.user.name} — FDNY Application Panel Active!")


@bot.command(name="attachpanel")
@commands.has_permissions(administrator=True)
async def attachpanel(ctx):
    embed = discord.Embed(
        title="🏢 NEW YORK CITY FIRE DEPARTMENT — APPLICATION CENTER",
        description=(
            "Welcome to the **FDNY Application Portal**!\n\n"
            "Please select the department division you wish to apply for using the dropdown menu below. "
            "You will receive your application details and link directly.\n\n"
            "**Available Divisions:**\n"
            "• 🚒 **Firefighter Program**\n"
            "• 🚑 **Emergency Medical Services (EMS)**\n"
            "• 📋 **Field Training Officer (FTO) Program** *(Requires FF III / Advanced EMT)*"
        ),
        color=discord.Color.dark_red()
    )
    await ctx.send(embed=embed, view=ApplicationPanelView())


# ==========================================================
# RUN BOT
# ==========================================================
bot.run("MTU2MDY0ODIxNTAwMTQ0MDM2Ng.GYa1V-.3czHdbqFzIv9y0XEm0cn0t6GVehJpWFNplTTdY")