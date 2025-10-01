import random
import json
import os
import logging
import threading
from queue import Queue
from logging.handlers import QueueHandler, QueueListener
from dotenv import load_dotenv
from groq import Groq

# Configure thread-safe logging
log_queue = Queue(-1)  # Unlimited queue
queue_handler = QueueHandler(log_queue)
file_handler = logging.FileHandler('groq_responses.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
listener = QueueListener(log_queue, file_handler)
listener.start()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(queue_handler)
logger.debug("Logging initialized for buildnovel.py with thread-safe QueueHandler")

# Load environment variables from .env file
load_dotenv()

class Agent:
    def __init__(self, name, personality, goals):
        self.name = name
        self.personality = personality
        self.goals = goals
        self.relationships = {}

    def interact(self, other_agent):
        base_score = random.uniform(-0.1, 0.1)
        if self.personality == "kind" and other_agent.personality == "kind":
            base_score += 0.2
        elif self.personality == "deceptive":
            base_score -= 0.1 if random.random() > 0.5 else 0.1
        self.relationships[other_agent.name] = self.relationships.get(other_agent.name, 0) + base_score
        other_agent.relationships[self.name] = other_agent.relationships.get(self.name, 0) + base_score
        logger.debug(f"Interaction: {self.name} ({self.personality}) <-> {other_agent.name} ({other_agent.personality}), change: {base_score:.2f}")
        return base_score

class Society:
    def __init__(self):
        self.agents = []
        self.event_graph = {
            "friendship": ["alliance", "betrayal", "romance"],
            "conflict": ["reconciliation", "escalation", "quest"],
            "neutral": ["friendship", "conflict", "romance"],
            "alliance": ["friendship", "betrayal"],
            "betrayal": ["conflict", "reconciliation"],
            "reconciliation": ["friendship", "neutral"],
            "escalation": ["conflict", "quest"],
            "romance": ["friendship", "betrayal"],
            "quest": ["neutral", "conflict"]
        }
        self.epochs = [
            {"name": "Paleolithic", "agent_add": 2, "theme": "primitive survival and basic bonds", "bias": "conflict"},
            {"name": "Neolithic", "agent_add": 3, "theme": "settlement and cooperation", "bias": "friendship"},
            {"name": "Bronze Age", "agent_add": 4, "theme": "trade and alliances", "bias": "alliance"},
            {"name": "Iron Age", "agent_add": 5, "theme": "wars and quests", "bias": "escalation"},
            {"name": "Industrial Era", "agent_add": 6, "theme": "innovation and betrayal", "bias": "quest"}
        ]
        self.chapters = []
        # Initialize Groq client once
        api_key = os.environ.get('GROQ_API_KEY')
        self.client = Groq(api_key=api_key) if api_key else None
        logger.debug(f"GROQ_API_KEY: {'set' if api_key else 'not set'}")

    def add_agent(self, agent):
        self.agents.append(agent)

    def generate_story(self, pages_per_epoch=5, algorithm="graph_based"):
        # Start with early humans
        self.agents = [
            Agent("Eve", "kind", "survive"),
            Agent("Adam", "ambitious", "explore")
        ]
        chapter_id = 0
        for epoch in self.epochs:
            logger.info(f"Starting epoch: {epoch['name']} with {len(self.agents)} agents")
            
            # Add new agents for population growth
            for _ in range(epoch["agent_add"]):
                new_name = f"Agent{len(self.agents) + 1}"
                new_personality = random.choice(["kind", "ambitious", "deceptive", "innovative"])
                new_goal = random.choice(["build", "conquer", "discover", "unite"])
                self.add_agent(Agent(new_name, new_personality, new_goal))
                logger.debug(f"Added agent: {new_name} ({new_personality}, goal: {new_goal})")

            # Generate chapter for this epoch
            chapter = self._generate_chapter(pages_per_epoch, algorithm, epoch, chapter_id)
            self.chapters.append(chapter)
            chapter_id += len(chapter)

        return self.chapters

    def _generate_chapter(self, num_pages, algorithm, epoch, chapter_id):
        current_event = {"type": "neutral"}
        pages = []
        for i in range(num_pages):
            agent1, agent2 = random.sample(self.agents, 2) if len(self.agents) >= 2 else (self.agents[0], self.agents[0])
            change = agent1.interact(agent2) if agent1 != agent2 else 0

            # Choose event type, with epoch bias
            if algorithm == "rule_based":
                event_type = "friendship" if change > 0 else "conflict"
            elif algorithm == "probabilistic":
                weights = [0.6 if change > 0 else 0.2, 0.3, 0.1]
                event_type = random.choices(["friendship", "conflict", "romance"], weights=weights)[0]
            elif algorithm == "graph_based":
                possible = self.event_graph.get(current_event["type"], ["neutral"])
                event_type = random.choice(possible)
            else:
                event_type = "neutral"
            
            # Apply epoch bias (override with 30% chance)
            if random.random() < 0.3:
                event_type = epoch["bias"]

            current_event = {
                "type": event_type,
                "agents": [agent1.name, agent2.name] if agent1 != agent2 else [agent1.name],
                "change": change,
                "epoch": epoch["name"]
            }

            # LLM for dialogue and choices
            narrative = self._call_llm(current_event, chapter_id + i, chapter_id + num_pages)
            logger.debug(f"Generated narrative for event {current_event['type']} (epoch {epoch['name']}, page {i}): {json.dumps(narrative, indent=2)}")

            # Audio based on event and epoch
            audio = []
            if i == 0:
                audio = [["PLAY", f"{epoch['name'].lower()}_{event_type}.mp3"]]
            elif i == num_pages - 1:
                audio = [["STOP", f"{epoch['name'].lower()}_{event_type}.mp3"]]

            # Images: epoch-themed backgrounds + agent sprites
            images = [f"{epoch['name'].lower()}_scene_{i+1}.png"]
            if len(current_event["agents"]) > 1:
                for agent in current_event["agents"]:
                    images += [f"{agent.lower()}_{epoch['name'].lower()}_{j}.png" for j in range(1, 5)]
            else:
                images += [f"{current_event['agents'][0].lower()}_{epoch['name'].lower()}_{j}.png" for j in range(1, 5)]

            # Build page
            page = [
                narrative["dialogue"],
                audio,
                images,
                narrative["choices"]
            ]
            pages.append(page)

        return {f"page{chapter_id + j}": page for j, page in enumerate(pages)}

    def _call_llm(self, event, page_idx, max_page):
        logger.debug(f"Calling LLM for event {event['type']} (epoch {event['epoch']}, page {page_idx})")
        
        if not self.client:
            logger.warning("Groq client not initialized (missing GROQ_API_KEY); using fallback narrative for event %s (epoch %s, page %d)", event['type'], event['epoch'], page_idx)
            narrative = {
                "dialogue": [
                    [event["agents"][0], f"In the {event['epoch']}, a {event['type']} stirs {event['agents'][0]}'s ancient soul.", 0],
                    ["Narrator", f"Their bond shifts like ancient sands: {event['change']:.2f}.", 0 if random.random() > 0.1 else 1]
                ],
                "choices": [
                    {"text": f"Embrace {event['type']} in {event['epoch']}", "next_page": f"page{page_idx+2}" if page_idx+2 < max_page else f"page{page_idx+1}"},
                    {"text": f"Resist {event['type']} in {event['epoch']}", "next_page": f"page{page_idx+3}" if page_idx+3 < max_page else f"page{page_idx+1}"}
                ] if page_idx < max_page - 1 else []
            }
            logger.debug(f"Fallback narrative for event {event['type']} (epoch {event['epoch']}, page {page_idx}): {json.dumps(narrative, indent=2)}")
            return narrative

        system_prompt = """
        You are a narrative generator for a visual novel about societal evolution from early humans. Generate 2-3 dialogue lines and 2 choices (if applicable) based on the event and epoch. Format strictly as JSON: {"dialogue": [["speaker", "text", flag], ...], "choices": [{"text": "Option", "next_page": "pageX"}, ...]}. Dialogue should be vivid, introspective, and surreal, fitting the epoch's theme (e.g., primitive for Paleolithic, innovative for Industrial). Use agent names or "Narrator". Set flag to 0 (visible) or 1 (hidden, 10% chance). Choices should reflect the event type, agent personalities, and epoch progression.
        """
        
        user_prompt = f"""
        Epoch: {event['epoch']} ({event['agents'][0]} (personality: {next((a.personality for a in self.agents if a.name == event['agents'][0]), 'unknown')}, goal: {next((a.goals for a in self.agents if a.name == event['agents'][0]), 'unknown')}), {', '.join([f"{agent} (personality: {next((a.personality for a in self.agents if a.name == agent), 'unknown')}, goal: {next((a.goals for a in self.agents if a.name == agent), 'unknown')} )" for agent in event['agents'][1:]]) if len(event['agents']) > 1 else ''}).
        Event: {event['type']}, relationship change: {event['change']:.2f}.
        Generate 2-3 dialogue lines and 2 branching choices (next_page as page{page_idx+2}/page{page_idx+3}). Keep it concise, surreal, and fitting the epoch's theme.
        """

        try:
            result = self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=250,
                temperature=0.8
            )
            content = result.choices[0].message.content.strip('```json\n').strip('```')
            logger.debug(f"Raw Groq content for event {event['type']} (epoch {event['epoch']}, page {page_idx}): {content}")
            logger.info(f"Groq API response for event {event['type']} (epoch {event['epoch']}, page {page_idx}): {json.dumps(result.to_dict(), indent=2)}")
            return json.loads(content)
        except Exception as e:
            logger.error(f"Groq API error for event {event['type']} (epoch {event['epoch']}, page {page_idx}): {str(e)}")
            narrative = {
                "dialogue": [
                    [event["agents"][0], f"In the {event['epoch']}, a {event['type']} stirs {event['agents'][0]}'s ancient soul.", 0],
                    ["Narrator", f"Their bond shifts like ancient sands: {event['change']:.2f}.", 0 if random.random() > 0.1 else 1]
                ],
                "choices": [
                    {"text": f"Embrace {event['type']} in {event['epoch']}", "next_page": f"page{page_idx+2}" if page_idx+2 < max_page else f"page{page_idx+1}"},
                    {"text": f"Resist {event['type']} in {event['epoch']}", "next_page": f"page{page_idx+3}" if page_idx+3 < max_page else f"page{page_idx+1}"}
                ] if page_idx < max_page - 1 else []
            }
            logger.debug(f"Fallback narrative for event {event['type']} (epoch {event['epoch']}, page {page_idx}): {json.dumps(narrative, indent=2)}")
            return narrative

if __name__ == "__main__":
    society = Society()
    timeline = society.generate_story(pages_per_epoch=5, algorithm="graph_based")
    with open("timeline.json", "w") as f:
        json.dump(timeline, f, indent=2)

    # Ensure logging is flushed before exit
    logger.handlers[0].queue.put(None)  # Signal listener to stop
    listener.stop()
    print("Generated timeline.json for VisualNovelEngine: Society Evolution Story!")