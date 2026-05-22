"""
AI-Powered Smart Calling & Lead Management Platform
====================================================
Automates customer interactions, captures leads efficiently,
and improves business communication and conversions.

Features:
- Lead capture & scoring
- AI-driven call simulation (via Claude API)
- Call scheduling & queue management
- Conversation logging & transcripts
- Analytics & conversion tracking
- CRM integration layer
"""

import json
import uuid
import random
import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum

# ─────────────────────────────────────────────
# ENUMS & CONSTANTS
# ─────────────────────────────────────────────

class LeadStatus(str, Enum):
    NEW        = "new"
    CONTACTED  = "contacted"
    QUALIFIED  = "qualified"
    CONVERTED  = "converted"
    LOST       = "lost"

class CallStatus(str, Enum):
    SCHEDULED  = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED  = "completed"
    FAILED     = "failed"
    NO_ANSWER  = "no_answer"

class Priority(str, Enum):
    LOW    = "low"
    MEDIUM = "medium"
    HIGH   = "high"
    URGENT = "urgent"


# ─────────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────────

@dataclass
class Lead:
    name: str
    phone: str
    email: str
    company: str = ""
    source: str = "website"
    status: LeadStatus = LeadStatus.NEW
    score: int = 0
    priority: Priority = Priority.MEDIUM
    notes: str = ""
    tags: list = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: str = field(
        default_factory=lambda: datetime.datetime.now().isoformat()
    )
    last_contacted: Optional[str] = None
    conversion_probability: float = 0.0

    def to_dict(self):
        return asdict(self)

    def __str__(self):
        return (
            f"Lead({self.id}) | {self.name} | {self.phone} | "
            f"Score: {self.score} | Status: {self.status.value}"
        )


@dataclass
class CallRecord:
    lead_id: str
    agent_name: str = "AI Agent"
    status: CallStatus = CallStatus.SCHEDULED
    scheduled_at: str = field(
        default_factory=lambda: datetime.datetime.now().isoformat()
    )
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    duration_seconds: int = 0
    transcript: list = field(default_factory=list)
    outcome: str = ""
    follow_up_required: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self):
        return asdict(self)

    def __str__(self):
        return (
            f"Call({self.id}) | Lead: {self.lead_id} | "
            f"Status: {self.status.value} | Duration: {self.duration_seconds}s"
        )


@dataclass
class Analytics:
    total_leads: int = 0
    leads_contacted: int = 0
    leads_converted: int = 0
    calls_made: int = 0
    calls_answered: int = 0
    average_call_duration: float = 0.0
    conversion_rate: float = 0.0
    best_performing_source: str = ""
    revenue_generated: float = 0.0


# ─────────────────────────────────────────────
# AI AGENT (Simulated — swap in real API call)
# ─────────────────────────────────────────────

class AICallAgent:
    """
    Simulates an AI voice agent conducting a sales/support call.
    In production: integrate with Twilio + Claude API for live calls.
    """

    SCRIPTS = {
        "intro": [
            "Hello {name}! This is Alex from {company}. I hope I caught you at a good time. "
            "I'm reaching out because we noticed you recently showed interest in our services.",
            "Hi {name}, this is Alex calling from {company}. I wanted to personally follow up "
            "on your inquiry and see how we can help you today.",
        ],
        "pitch": [
            "We help businesses like yours increase conversions by up to 40% using AI-driven "
            "automation. I'd love to show you how it works.",
            "Our platform has helped over 500 companies streamline their lead management and "
            "reduce response time by 60%. Does that sound relevant to your goals?",
        ],
        "objection_price": [
            "I completely understand budget concerns. What if I told you our ROI typically "
            "pays for the platform within the first month?",
            "That's a fair point. We do offer flexible pricing tiers and a 14-day free trial "
            "so you can experience the value before committing.",
        ],
        "objection_time": [
            "I appreciate you being upfront about that. The good news is setup takes less than "
            "an hour, and most clients see results within the first week.",
            "Understood. Would a 10-minute demo next week work? I can show you exactly how it "
            "fits into your existing workflow.",
        ],
        "close": [
            "Based on what you've shared, I think we're a great fit. Can I go ahead and set "
            "up a demo call for you with our product specialist?",
            "It sounds like our platform could really solve your challenges. Are you ready to "
            "start a free trial today?",
        ],
        "wrap_up": [
            "Perfect! I'll send the details to your email right away. Looking forward to "
            "helping you grow. Have a wonderful day, {name}!",
            "Excellent! You'll receive a confirmation shortly. Our team is excited to work "
            "with you. Talk soon!",
        ],
    }

    CUSTOMER_RESPONSES = [
        ("I'm interested, tell me more.", "positive"),
        ("We don't have budget right now.", "objection_price"),
        ("I'm too busy at the moment.", "objection_time"),
        ("Sure, I'll consider it.", "neutral"),
        ("Yes, let's schedule a demo!", "positive"),
        ("How much does it cost?", "objection_price"),
        ("Send me more information by email.", "neutral"),
        ("We already use a competitor.", "objection_price"),
    ]

    def conduct_call(self, lead: Lead, company_name: str = "TechCorp") -> CallRecord:
        record = CallRecord(lead_id=lead.id)
        record.status = CallStatus.IN_PROGRESS
        record.started_at = datetime.datetime.now().isoformat()

        transcript = []
        steps = ["intro", "pitch", None, "close", "wrap_up"]
        outcome = "no_decision"

        for step in steps:
            if step is None:
                # Customer objection/response step
                response, response_type = random.choice(self.CUSTOMER_RESPONSES)
                transcript.append({"speaker": "Customer", "text": response})
                if response_type == "positive":
                    outcome = "interested"
                elif response_type.startswith("objection"):
                    rebuttal = random.choice(self.SCRIPTS[response_type])
                    transcript.append({"speaker": "AI Agent", "text": rebuttal})
                continue

            script_lines = self.SCRIPTS.get(step, [])
            if script_lines:
                line = random.choice(script_lines).format(
                    name=lead.name.split()[0],
                    company=company_name
                )
                transcript.append({"speaker": "AI Agent", "text": line})

        record.ended_at = datetime.datetime.now().isoformat()
        record.duration_seconds = random.randint(60, 420)
        record.transcript = transcript
        record.status = CallStatus.COMPLETED
        record.outcome = outcome
        record.follow_up_required = outcome in ("interested", "no_decision")

        return record


# ─────────────────────────────────────────────
# LEAD SCORING ENGINE
# ─────────────────────────────────────────────

class LeadScoringEngine:
    """
    Scores leads 0–100 based on engagement signals.
    Higher score = higher conversion likelihood.
    """

    SOURCE_SCORES = {
        "referral": 30,
        "demo_request": 25,
        "paid_ad": 20,
        "organic_search": 15,
        "website": 10,
        "cold_outreach": 5,
        "social_media": 12,
    }

    TAG_SCORES = {
        "decision_maker": 20,
        "enterprise": 18,
        "hot_lead": 15,
        "repeat_visitor": 10,
        "downloaded_content": 8,
        "webinar_attendee": 12,
        "free_trial": 14,
    }

    def score(self, lead: Lead) -> int:
        score = self.SOURCE_SCORES.get(lead.source.lower(), 5)

        for tag in lead.tags:
            score += self.TAG_SCORES.get(tag.lower(), 0)

        if lead.company:
            score += 5

        if lead.last_contacted:
            score += 8

        score += random.randint(0, 10)  # engagement noise
        score = min(score, 100)
        return score

    def conversion_probability(self, score: int) -> float:
        if score >= 80:
            return round(random.uniform(0.70, 0.95), 2)
        elif score >= 60:
            return round(random.uniform(0.40, 0.70), 2)
        elif score >= 40:
            return round(random.uniform(0.20, 0.40), 2)
        else:
            return round(random.uniform(0.05, 0.20), 2)

    def priority(self, score: int) -> Priority:
        if score >= 75:
            return Priority.URGENT
        elif score >= 55:
            return Priority.HIGH
        elif score >= 35:
            return Priority.MEDIUM
        else:
            return Priority.LOW


# ─────────────────────────────────────────────
# CALL SCHEDULER
# ─────────────────────────────────────────────

class CallScheduler:
    """Manages call queue, prioritization, and scheduling."""

    def __init__(self):
        self.queue: list[tuple[Priority, Lead]] = []
        self._priority_order = {
            Priority.URGENT: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3,
        }

    def enqueue(self, lead: Lead):
        self.queue.append((lead.priority, lead))
        self.queue.sort(key=lambda x: self._priority_order[x[0]])

    def dequeue(self) -> Optional[Lead]:
        if self.queue:
            _, lead = self.queue.pop(0)
            return lead
        return None

    def peek_next(self) -> Optional[Lead]:
        return self.queue[0][1] if self.queue else None

    def queue_size(self) -> int:
        return len(self.queue)

    def queue_summary(self) -> dict:
        summary = {p.value: 0 for p in Priority}
        for priority, _ in self.queue:
            summary[priority.value] += 1
        return summary


# ─────────────────────────────────────────────
# PLATFORM CORE
# ─────────────────────────────────────────────

class SmartCallingPlatform:
    """
    Central orchestrator for the AI-powered calling platform.
    Manages leads, calls, scoring, scheduling, and analytics.
    """

    def __init__(self, company_name: str = "SmartCaller"):
        self.company_name = company_name
        self.leads: dict[str, Lead] = {}
        self.call_records: dict[str, CallRecord] = {}
        self.scorer = LeadScoringEngine()
        self.scheduler = CallScheduler()
        self.agent = AICallAgent()
        print(f"\n{'='*60}")
        print(f"  🤖  {company_name} — AI Calling Platform  🤖")
        print(f"{'='*60}\n")

    # ── Lead Management ──────────────────────

    def add_lead(self, **kwargs) -> Lead:
        lead = Lead(**kwargs)
        lead.score = self.scorer.score(lead)
        lead.priority = self.scorer.priority(lead.score)
        lead.conversion_probability = self.scorer.conversion_probability(lead.score)
        self.leads[lead.id] = lead
        self.scheduler.enqueue(lead)
        print(f"  ✅ Lead Added    → {lead}")
        return lead

    def update_lead_status(self, lead_id: str, status: LeadStatus):
        if lead_id in self.leads:
            self.leads[lead_id].status = status
            print(f"  🔄 Lead {lead_id} status → {status.value}")

    def get_lead(self, lead_id: str) -> Optional[Lead]:
        return self.leads.get(lead_id)

    def filter_leads(
        self,
        status: Optional[LeadStatus] = None,
        min_score: int = 0,
        priority: Optional[Priority] = None,
    ) -> list[Lead]:
        results = list(self.leads.values())
        if status:
            results = [l for l in results if l.status == status]
        if priority:
            results = [l for l in results if l.priority == priority]
        results = [l for l in results if l.score >= min_score]
        return sorted(results, key=lambda l: l.score, reverse=True)

    # ── Calling ──────────────────────────────

    def make_call(self, lead_id: str) -> Optional[CallRecord]:
        lead = self.leads.get(lead_id)
        if not lead:
            print(f"  ❌ Lead {lead_id} not found.")
            return None

        print(f"\n  📞 Initiating call → {lead.name} ({lead.phone})")
        record = self.agent.conduct_call(lead, self.company_name)
        self.call_records[record.id] = record

        lead.last_contacted = datetime.datetime.now().isoformat()
        lead.status = LeadStatus.CONTACTED

        if record.outcome == "interested":
            lead.status = LeadStatus.QUALIFIED
            lead.score = min(lead.score + 15, 100)
            lead.conversion_probability = self.scorer.conversion_probability(lead.score)

        print(f"  ✅ Call Complete  → Outcome: {record.outcome} | "
              f"Duration: {record.duration_seconds}s | "
              f"Follow-up: {record.follow_up_required}")
        return record

    def run_call_queue(self, max_calls: int = 5):
        print(f"\n  🚀 Running Call Queue  (max: {max_calls} calls)")
        print(f"  Queue: {self.scheduler.queue_summary()}\n")
        processed = 0
        while processed < max_calls and self.scheduler.queue_size() > 0:
            lead = self.scheduler.dequeue()
            if lead:
                self.make_call(lead.id)
                processed += 1
        print(f"\n  ✅ Queue run complete. Calls processed: {processed}")

    # ── Transcripts ──────────────────────────

    def print_transcript(self, call_id: str):
        record = self.call_records.get(call_id)
        if not record:
            print(f"  ❌ Call {call_id} not found.")
            return
        print(f"\n  📋 Transcript — Call {call_id}")
        print(f"  {'─'*50}")
        for turn in record.transcript:
            speaker = turn["speaker"]
            text = turn["text"]
            icon = "🤖" if speaker == "AI Agent" else "👤"
            print(f"  {icon} [{speaker}]: {text}")
        print(f"  {'─'*50}")
        print(f"  Outcome: {record.outcome} | Follow-up: {record.follow_up_required}\n")

    # ── Analytics ────────────────────────────

    def get_analytics(self) -> Analytics:
        a = Analytics()
        a.total_leads = len(self.leads)
        a.leads_contacted = sum(
            1 for l in self.leads.values()
            if l.status != LeadStatus.NEW
        )
        a.leads_converted = sum(
            1 for l in self.leads.values()
            if l.status == LeadStatus.CONVERTED
        )
        a.calls_made = len(self.call_records)
        a.calls_answered = sum(
            1 for c in self.call_records.values()
            if c.status == CallStatus.COMPLETED
        )
        durations = [c.duration_seconds for c in self.call_records.values() if c.duration_seconds]
        a.average_call_duration = round(sum(durations) / len(durations), 1) if durations else 0
        a.conversion_rate = (
            round(a.leads_converted / a.total_leads * 100, 1) if a.total_leads else 0
        )

        # Best source
        source_counts: dict[str, int] = {}
        for lead in self.leads.values():
            source_counts[lead.source] = source_counts.get(lead.source, 0) + 1
        a.best_performing_source = max(source_counts, key=source_counts.get) if source_counts else ""

        return a

    def print_dashboard(self):
        a = self.get_analytics()
        print(f"\n{'='*60}")
        print(f"  📊  PLATFORM DASHBOARD — {self.company_name}")
        print(f"{'='*60}")
        print(f"  Total Leads          : {a.total_leads}")
        print(f"  Leads Contacted      : {a.leads_contacted}")
        print(f"  Leads Converted      : {a.leads_converted}")
        print(f"  Conversion Rate      : {a.conversion_rate}%")
        print(f"  Calls Made           : {a.calls_made}")
        print(f"  Calls Answered       : {a.calls_answered}")
        print(f"  Avg Call Duration    : {a.average_call_duration}s")
        print(f"  Best Lead Source     : {a.best_performing_source}")

        print(f"\n  🔝 Top 5 Leads by Score:")
        top = sorted(self.leads.values(), key=lambda l: l.score, reverse=True)[:5]
        for l in top:
            bar = "█" * (l.score // 10) + "░" * (10 - l.score // 10)
            prob = f"{int(l.conversion_probability * 100)}%"
            print(f"    [{bar}] {l.score:3d} | {prob:4s} | {l.name:<20} | {l.priority.value}")
        print(f"{'='*60}\n")

    # ── Export ───────────────────────────────

    def export_leads(self, filepath: str = "leads_export.json"):
        data = [l.to_dict() for l in self.leads.values()]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  💾 Leads exported → {filepath}")

    def export_calls(self, filepath: str = "calls_export.json"):
        data = [c.to_dict() for c in self.call_records.values()]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  💾 Calls exported → {filepath}")


# ─────────────────────────────────────────────
# DEMO / MAIN
# ─────────────────────────────────────────────

def run_demo():
    platform = SmartCallingPlatform(company_name="NexusAI")

    # ── Seed sample leads ──
    sample_leads = [
        dict(name="Sarah Mitchell",   phone="+1-555-0101", email="sarah@techcorp.com",
             company="TechCorp",      source="demo_request",  tags=["decision_maker", "enterprise"]),
        dict(name="James Okafor",     phone="+1-555-0102", email="james@startupxyz.io",
             company="StartupXYZ",   source="referral",       tags=["hot_lead", "free_trial"]),
        dict(name="Priya Sharma",     phone="+1-555-0103", email="priya@innovate.in",
             company="Innovate Ltd",  source="organic_search", tags=["webinar_attendee"]),
        dict(name="Carlos Rivera",    phone="+1-555-0104", email="carlos@retailco.mx",
             company="RetailCo",     source="paid_ad",         tags=["downloaded_content"]),
        dict(name="Emma Lindqvist",   phone="+1-555-0105", email="emma@nordictrade.se",
             company="Nordic Trade", source="cold_outreach",   tags=[]),
        dict(name="David Chen",       phone="+1-555-0106", email="david@cloudbase.ai",
             company="CloudBase",    source="referral",         tags=["decision_maker", "hot_lead"]),
        dict(name="Fatima Al-Hassan", phone="+1-555-0107", email="fatima@medgroup.ae",
             company="MedGroup",     source="website",          tags=["repeat_visitor"]),
        dict(name="Luca Bianchi",     phone="+1-555-0108", email="luca@finserv.it",
             company="FinServ",      source="demo_request",     tags=["enterprise", "free_trial"]),
    ]

    print("\n  📥 Ingesting Leads...")
    for data in sample_leads:
        platform.add_lead(**data)

    # ── Run the call queue ──
    print(f"\n{'─'*60}")
    platform.run_call_queue(max_calls=4)

    # ── Show a transcript ──
    if platform.call_records:
        first_call_id = list(platform.call_records.keys())[0]
        platform.print_transcript(first_call_id)

    # ── Mark one as converted ──
    if platform.leads:
        first_lead_id = list(platform.leads.keys())[0]
        platform.update_lead_status(first_lead_id, LeadStatus.CONVERTED)

    # ── Dashboard ──
    platform.print_dashboard()

    # ── Export data ──
    platform.export_leads("/tmp/leads_export.json")
    platform.export_calls("/tmp/calls_export.json")

    print("\n  🎉 Platform demo complete!\n")


if __name__ == "__main__":
    run_demo()
