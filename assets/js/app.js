const STORAGE_KEY = "acuite-connect-state-v1";

const gradients = {
  warm: "var(--grad-warm)",
  cool: "var(--grad-cool)",
  sun: "var(--grad-sun)",
  fire: "var(--grad-fire)",
  leaf: "linear-gradient(135deg,var(--green),var(--lime))",
  gold: "linear-gradient(135deg,var(--yellow),var(--amber))",
  ember: "linear-gradient(135deg,var(--orange),var(--maroon))",
  mixed: "linear-gradient(135deg,var(--lime),var(--yellow),var(--amber))",
};

const appData = {
  currentUser: {
    name: "Rahul Mehta",
    initials: "RM",
    role: "Senior Analyst - Ratings",
    city: "Mumbai",
  },
  agenda: [
    {
      id: "agenda-committee-huddle",
      time: "11:30 AM",
      title: "Committee prep huddle",
      meta: "Infrastructure team - Meeting Room 2",
    },
    {
      id: "agenda-surveillance",
      time: "2:00 PM",
      title: "NBFC surveillance review",
      meta: "With Priya Sharma and Karthik Iyer",
    },
    {
      id: "agenda-learning",
      time: "4:30 PM",
      title: "Writing standards learning sprint",
      meta: "45 min session - Research floor",
    },
  ],
  tasks: [
    {
      id: "task-committee-note",
      title: "Finalize committee note for Sunrise Infra",
      due: "Due today",
      priority: "high",
    },
    {
      id: "task-vendor-review",
      title: "Review vendor onboarding request",
      due: "Due tomorrow",
      priority: "medium",
    },
    {
      id: "task-spotlight",
      title: "Nominate a teammate for Spotlight",
      due: "This week",
      priority: "low",
    },
  ],
  pulse: [
    { id: "pulse-tools", value: "6", label: "Tools mapped for launch" },
    { id: "pulse-posts", value: "14", label: "Fresh updates this week" },
    { id: "pulse-clubs", value: "11", label: "Active communities" },
    { id: "pulse-resources", value: "32", label: "Resources ready to index" },
  ],
  quickTools: [
    {
      id: "tool-karma",
      name: "Acuité Karma",
      initials: "AK",
      summary: "Track actions, owners and weekly follow-ups.",
      status: "live",
      note: "2 matters awaiting updates",
      gradient: "warm",
      url: "https://karma.acuite-group.com",
    },
    {
      id: "tool-mymeetings",
      name: "MyMeetings",
      initials: "MM",
      summary: "Capture minutes, action items and meeting reports.",
      status: "pilot",
      note: "Rollout-ready for pilot teams",
      gradient: "cool",
      message: "MyMeetings is positioned as the next linked workflow inside Connect.",
    },
    {
      id: "tool-krishna",
      name: "Krishna AAA",
      initials: "KA",
      summary: "Drafting and process support for Acuité analysts.",
      status: "pilot",
      note: "Great fit for analyst workflows",
      gradient: "fire",
      message: "Krishna AAA is marked for pilot integration into the tool hub.",
    },
    {
      id: "tool-people",
      name: "People Desk",
      initials: "PD",
      summary: "Find experts by sector, city and capability.",
      status: "pilot",
      note: "Backed by the new directory panel",
      gradient: "gold",
      tab: "directory",
    },
    {
      id: "tool-knowledge",
      name: "Knowledge Hub",
      initials: "KH",
      summary: "Policies, templates, decks and archived notes.",
      status: "pilot",
      note: "A good next home for institutional memory",
      gradient: "mixed",
      tab: "knowledge",
    },
    {
      id: "tool-helpdesk",
      name: "Help Desk",
      initials: "HD",
      summary: "Single front door for HR, IT and admin requests.",
      status: "planned",
      note: "Ideal for the next workflow layer",
      gradient: "ember",
      message: "Help Desk is shown as a planned module in this MVP foundation.",
    },
  ],
  homePosts: [
    {
      id: "post-townhall",
      kind: "standard",
      variant: "pinned",
      category: "events",
      title: "Town Hall - Q4 results presentation",
      body: [
        "Join us on March 25 at 4:00 PM in the Mumbai auditorium. Leadership will share Q4 results, priorities for the new quarter, and the first roadmap for Acuité Connect.",
      ],
      authorName: "HR Team",
      authorMeta: "2 hours ago",
      initials: "HR",
      avatar: "sun",
      likes: 24,
      comments: 8,
      actionLabel: "Open bulletin",
      actionTab: "bulletin",
    },
    {
      id: "post-kudos-karthik",
      kind: "kudos",
      giver: "Ananya Rao",
      recipient: "Karthik Iyer",
      recipientRole: "Associate Analyst - Ratings",
      tagId: "analysis",
      message: "Karthik's analysis on NBFCs was incredibly thorough. His diligence directly shaped the rating committee discussion.",
      initials: "KI",
      avatar: "cool",
      likes: 31,
    },
    {
      id: "post-research-fy27",
      kind: "standard",
      variant: "default",
      category: "announcements",
      title: "Infrastructure outlook for FY27 is now live",
      body: [
        "The capex cycle is showing real momentum and there are important credit quality signals emerging in mid-market infrastructure. The note is now in the research portal.",
      ],
      authorName: "Neha Srinivasan",
      authorMeta: "VP - Research - 5h ago",
      initials: "NS",
      avatar: "fire",
      likes: 18,
      comments: 12,
      actionLabel: "Save to knowledge",
      actionMessage: "This note would be a strong early candidate for the Knowledge Hub.",
    },
    {
      id: "post-welcome-arjun",
      kind: "standard",
      variant: "welcome",
      category: "announcements",
      title: "Welcome aboard, Arjun Nair",
      body: [
        "Arjun joins as Analyst - Structured Finance in Mumbai. Previously with CRISIL, he brings three years of securitisation ratings experience.",
      ],
      authorName: "People Team",
      authorMeta: "Today",
      initials: "PT",
      avatar: "leaf",
      likes: 42,
      comments: 3,
    },
    {
      id: "post-priya-milestone",
      kind: "standard",
      variant: "milestone",
      category: "announcements",
      title: "Priya Sharma completes 5 years at Acuité",
      body: [
        "From Senior Analyst to leading financial institutions coverage, Priya's journey has shaped both practice quality and team mentorship.",
      ],
      authorName: "Leadership Desk",
      authorMeta: "Yesterday",
      initials: "LD",
      avatar: "gold",
      likes: 56,
      comments: 9,
    },
  ],
  bulletinPosts: [
    {
      id: "bulletin-connect-beta",
      kind: "standard",
      variant: "pinned",
      category: "announcements",
      title: "Acuité Connect beta is now open for internal feedback",
      body: [
        "This is the first pass at turning the social prototype into a practical employee workspace. Please explore the new directory, tool hub, and knowledge sections.",
      ],
      authorName: "Internal Comms",
      authorMeta: "1 day ago",
      initials: "IC",
      avatar: "fire",
      likes: 89,
      comments: 23,
    },
    {
      id: "bulletin-townhall",
      kind: "standard",
      variant: "default",
      category: "events",
      title: "Town hall agenda shared",
      body: [
        "Q4 highlights, business outlook, hiring updates, and a short demo of the next wave of internal tools are all on the March 25 agenda.",
      ],
      authorName: "MD Office",
      authorMeta: "1 day ago",
      initials: "MD",
      avatar: "sun",
      likes: 54,
      comments: 10,
    },
    {
      id: "bulletin-leave-planner",
      kind: "standard",
      variant: "default",
      category: "hr",
      title: "Quarter 1 leave planner is open",
      body: [
        "Managers can now review leave plans for April to June. Teams should aim to lock key dates before the next scheduling cycle.",
      ],
      authorName: "HR Operations",
      authorMeta: "2 days ago",
      initials: "HR",
      avatar: "cool",
      likes: 21,
      comments: 5,
    },
    {
      id: "bulletin-learning-calendar",
      kind: "standard",
      variant: "default",
      category: "events",
      title: "Learning calendar for the quarter is published",
      body: [
        "Writing standards, model review, and sector deep-dives are now scheduled. The long-term plan is to move these into the Knowledge Hub.",
      ],
      authorName: "Learning Cell",
      authorMeta: "3 days ago",
      initials: "LC",
      avatar: "leaf",
      likes: 32,
      comments: 4,
    },
  ],
  wallPosts: [
    {
      id: "wall-rohan",
      kind: "kudos",
      giver: "Meera Gupta",
      recipient: "Rohan Deshmukh",
      recipientRole: "Analyst - Corporate Ratings",
      tagId: "teamwork",
      message: "Rohan stayed back three nights to help meet the surveillance deadline. It was not even his mandate. That is real team play.",
      initials: "RD",
      avatar: "warm",
      likes: 27,
    },
    {
      id: "wall-sneha",
      kind: "kudos",
      giver: "Priya Sharma",
      recipient: "Sneha Patil",
      recipientRole: "Compliance",
      tagId: "client",
      message: "Sneha kept client communication calm, clear and proactive while we were handling a tight turnaround. She made everyone look good.",
      initials: "SP",
      avatar: "cool",
      likes: 19,
    },
    {
      id: "wall-neha",
      kind: "kudos",
      giver: "Vikram Joshi",
      recipient: "Neha Srinivasan",
      recipientRole: "VP - Research",
      tagId: "mentor",
      message: "Neha turned a rough draft into a real piece of analysis in one review session. She teaches without making people nervous.",
      initials: "NS",
      avatar: "fire",
      likes: 33,
    },
  ],
  leaderboard: [
    { id: "lb-priya", name: "Priya Sharma", count: 16 },
    { id: "lb-neha", name: "Neha Srinivasan", count: 14 },
    { id: "lb-karthik", name: "Karthik Iyer", count: 11 },
    { id: "lb-sneha", name: "Sneha Patil", count: 9 },
  ],
  clubs: [
    {
      id: "club-cricket",
      name: "Cricket Club",
      description: "Weekend matches, IPL banter and tournaments.",
      emoji: "🏏",
      background: "linear-gradient(135deg,var(--green),var(--lime))",
      members: 48,
      defaultJoined: true,
      nextEvent: "Practice nets - Friday 6:30 PM",
      avatars: [
        { initials: "AK", gradient: "leaf" },
        { initials: "RD", gradient: "warm" },
        { initials: "SP", gradient: "gold" },
      ],
    },
    {
      id: "club-book",
      name: "Book Club",
      description: "Monthly picks, recommendations and quick reviews.",
      emoji: "📚",
      background: "linear-gradient(135deg,var(--maroon),var(--orange))",
      members: 22,
      defaultJoined: false,
      nextEvent: "March pick discussion - Thursday",
      avatars: [
        { initials: "NS", gradient: "ember" },
        { initials: "MG", gradient: "gold" },
      ],
    },
    {
      id: "club-markets",
      name: "Markets After Hours",
      description: "Macro views, market moves and investing chat.",
      emoji: "📈",
      background: "linear-gradient(135deg,var(--amber),var(--yellow))",
      members: 35,
      defaultJoined: false,
      nextEvent: "Global rates round-up - Monday",
      avatars: [
        { initials: "VJ", gradient: "ember" },
        { initials: "KI", gradient: "leaf" },
      ],
    },
    {
      id: "club-fitness",
      name: "Fitness and Running",
      description: "Challenges, workout plans and accountability buddies.",
      emoji: "🏃",
      background: "linear-gradient(135deg,var(--lime),var(--green))",
      members: 19,
      defaultJoined: true,
      nextEvent: "Marine Drive 5K - Sunday",
      avatars: [
        { initials: "PS", gradient: "warm" },
        { initials: "RM", gradient: "gold" },
      ],
    },
    {
      id: "club-food",
      name: "Foodies",
      description: "Reviews, recipes, lunch lists and potlucks.",
      emoji: "🍳",
      background: "linear-gradient(135deg,var(--orange),var(--maroon))",
      members: 31,
      defaultJoined: false,
      nextEvent: "Street food walk - next Wednesday",
      avatars: [
        { initials: "SP", gradient: "ember" },
      ],
    },
    {
      id: "club-photo",
      name: "Photography",
      description: "Photo walks, phone camera hacks and shared albums.",
      emoji: "📷",
      background: "linear-gradient(135deg,var(--yellow),var(--lime))",
      members: 14,
      defaultJoined: false,
      nextEvent: "Golden hour walk - Saturday",
      avatars: [
        { initials: "MG", gradient: "gold" },
      ],
    },
  ],
  spotlights: [
    {
      id: "spotlight-neha",
      name: "Neha Srinivasan",
      role: "VP - Research - 7 years",
      initials: "NS",
      photoGradient: "fire",
      qa: [
        {
          question: "Favourite part about Acuité?",
          answer: "The intellectual honesty. In ratings, you cannot cut corners - and here, nobody asks you to.",
        },
        {
          question: "Something people do not know?",
          answer: "I am a competitive Scrabble player and represented Maharashtra at nationals twice.",
        },
        {
          question: "Best advice received?",
          answer: "The data does not lie, but it does not tell you the whole truth. That line changed how I approach credit analysis.",
        },
      ],
    },
    {
      id: "spotlight-vikram",
      name: "Vikram Joshi",
      role: "AVP - Ratings",
      initials: "VJ",
      photoGradient: "cool",
    },
    {
      id: "spotlight-sneha",
      name: "Sneha Patil",
      role: "Compliance",
      initials: "SP",
      photoGradient: "sun",
    },
    {
      id: "spotlight-amit",
      name: "Amit Kumar",
      role: "SME Ratings",
      initials: "AK",
      photoGradient: "fire",
    },
  ],
  pitches: [
    {
      id: "pitch-exchange",
      title: "Analyst exchange across offices",
      description: "Create 2-week rotations between offices every quarter to cross-pollinate knowledge and build stronger networks.",
      author: "Karthik Iyer",
      comments: 14,
      status: "review",
      votes: 34,
      defaultUpvoted: true,
      createdAt: 1,
    },
    {
      id: "pitch-podcast",
      title: "Internal podcast - The Rating Room",
      description: "A monthly 20-minute audio series on interesting rating cases, anonymised for learning and perfect for commutes.",
      author: "Rahul Mehta",
      comments: 9,
      status: "submitted",
      votes: 28,
      defaultUpvoted: false,
      createdAt: 2,
    },
    {
      id: "pitch-flex-friday",
      title: "Flex Friday afternoons for learning",
      description: "Reserve time after 3 PM on Fridays for courses, CFA prep, webinars and internal learning, without meetings.",
      author: "Priya Sharma",
      comments: 22,
      status: "approved",
      votes: 45,
      defaultUpvoted: false,
      createdAt: 3,
    },
    {
      id: "pitch-standing-desks",
      title: "Standing desks and ergonomic chairs",
      description: "A simple health investment for people who spend 10+ hours at desks across ratings, research and operations.",
      author: "Sneha Patil",
      comments: 31,
      status: "implemented",
      votes: 52,
      defaultUpvoted: false,
      createdAt: 4,
    },
    {
      id: "pitch-expertise-map",
      title: "A sector expertise map inside Connect",
      description: "Make it easy to find who knows what by sector, skill, city and recent mandates. This is partly what the new directory starts to solve.",
      author: "Riya Desai",
      comments: 7,
      status: "submitted",
      votes: 19,
      defaultUpvoted: false,
      createdAt: 5,
    },
  ],
  moments: [
    { id: "moment-cricket", title: "Cricket Tournament", photos: 12, category: "events", emoji: "🏏", background: "linear-gradient(135deg,var(--green),var(--lime))" },
    { id: "moment-annual-day", title: "Annual Day", photos: 34, category: "events", emoji: "🎊", background: "linear-gradient(135deg,var(--orange),var(--maroon))" },
    { id: "moment-lonavala", title: "Offsite Lonavala", photos: 28, category: "outings", emoji: "🏔️", background: "linear-gradient(135deg,var(--lime),var(--yellow))" },
    { id: "moment-townhall", title: "Town Hall", photos: 8, category: "office", emoji: "🎤", background: "linear-gradient(135deg,var(--amber),var(--orange))" },
    { id: "moment-diwali", title: "Diwali", photos: 22, category: "events", emoji: "🪔", background: "linear-gradient(135deg,var(--maroon),var(--orange))" },
    { id: "moment-birthdays", title: "Birthdays", photos: 15, category: "office", emoji: "🎂", background: "linear-gradient(135deg,var(--yellow),var(--amber))" },
    { id: "moment-training", title: "Training Week", photos: 10, category: "office", emoji: "📊", background: "linear-gradient(135deg,var(--green),var(--amber))" },
    { id: "moment-awards", title: "Awards Night", photos: 40, category: "events", emoji: "🏆", background: "linear-gradient(135deg,var(--orange),var(--yellow))" },
  ],
  alumni: [
    { id: "alumni-deepak", name: "Deepak Khanna", current: "Director - ICRA", batch: "2019", tenure: "4 yrs - Ratings", initials: "DK", gradient: "warm" },
    { id: "alumni-swati", name: "Swati Agarwal", current: "VP - JP Morgan", batch: "2020", tenure: "3 yrs - Research", initials: "SA", gradient: "cool" },
    { id: "alumni-rajesh", name: "Rajesh Patel", current: "Co-founder - FinScore", batch: "2018", tenure: "5 yrs - Analytics", initials: "RP", gradient: "fire" },
    { id: "alumni-nidhi", name: "Nidhi Menon", current: "AVP - Kotak", batch: "2021", tenure: "2 yrs - Ratings", initials: "NM", gradient: "sun" },
    { id: "alumni-arun", name: "Arun Thakur", current: "S&P Global", batch: "2022", tenure: "3 yrs - Structured Finance", initials: "AT", gradient: "leaf" },
    { id: "alumni-pooja", name: "Pooja Ghosh", current: "MBA - ISB", batch: "2023", tenure: "2 yrs - Compliance", initials: "PG", gradient: "gold" },
  ],
  directory: [
    {
      id: "person-rahul",
      name: "Rahul Mehta",
      role: "Senior Analyst - Ratings",
      city: "Mumbai",
      category: "ratings",
      initials: "RM",
      gradient: "warm",
      blurb: "Strong on committee notes, issuer narratives and financial institution comparisons.",
      teams: ["Ratings", "Financial Institutions"],
      skills: ["Committee prep", "Issuer notes", "Presentation decks"],
      availability: "Available for deal review huddles",
    },
    {
      id: "person-neha",
      name: "Neha Srinivasan",
      role: "VP - Research",
      city: "Mumbai",
      category: "research",
      initials: "NS",
      gradient: "fire",
      blurb: "Leads long-form research, analyst coaching and sector thought pieces.",
      teams: ["Research", "Infrastructure"],
      skills: ["Long-form research", "Mentoring", "Sector outlooks"],
      availability: "Best for research framing and reviews",
    },
    {
      id: "person-karthik",
      name: "Karthik Iyer",
      role: "Associate Analyst - Ratings",
      city: "Bengaluru",
      category: "ratings",
      initials: "KI",
      gradient: "cool",
      blurb: "Known for sharp modelling support on NBFC and mid-market credit work.",
      teams: ["Ratings", "NBFC"],
      skills: ["Modelling", "Surveillance", "Data cleanup"],
      availability: "Open for peer reviews",
    },
    {
      id: "person-sneha",
      name: "Sneha Patil",
      role: "Compliance Manager",
      city: "Mumbai",
      category: "people",
      initials: "SP",
      gradient: "gold",
      blurb: "Keeps process, policy and client-facing coordination tidy and calm.",
      teams: ["Compliance", "Governance"],
      skills: ["Policy queries", "Escalations", "Client coordination"],
      availability: "Best for policy and process checks",
    },
    {
      id: "person-priya",
      name: "Priya Sharma",
      role: "Director - Financial Institutions",
      city: "Mumbai",
      category: "ratings",
      initials: "PS",
      gradient: "warm",
      blurb: "Leads FI coverage and is frequently the fastest reviewer for difficult committee notes.",
      teams: ["Ratings", "Financial Institutions"],
      skills: ["Committee leadership", "Bank ratings", "Reviewer feedback"],
      availability: "Leadership reviews on request",
    },
    {
      id: "person-riya",
      name: "Riya Desai",
      role: "Associate - Data and Analytics",
      city: "Pune",
      category: "ops",
      initials: "RD",
      gradient: "leaf",
      blurb: "Bridges analyst needs with data cleaning, trackers and dashboard support.",
      teams: ["Analytics", "Operations"],
      skills: ["Dashboards", "Data QA", "Tracker design"],
      availability: "Good first stop for dashboard ideas",
    },
    {
      id: "person-arjun",
      name: "Arjun Nair",
      role: "Analyst - Structured Finance",
      city: "Mumbai",
      category: "ratings",
      initials: "AN",
      gradient: "sun",
      blurb: "New joiner with securitisation coverage experience and structured product instincts.",
      teams: ["Ratings", "Structured Finance"],
      skills: ["Securitisation", "Waterfall review", "New issue notes"],
      availability: "Actively onboarding this quarter",
    },
    {
      id: "person-reshma",
      name: "Reshma Polasa",
      role: "Head - Operations",
      city: "Hyderabad",
      category: "ops",
      initials: "RP",
      gradient: "ember",
      blurb: "Great at unblocking cross-team process issues and building smoother workflows.",
      teams: ["Operations", "Process"],
      skills: ["Workflow design", "Ownership mapping", "Process fixes"],
      availability: "Ideal for operational bottlenecks",
    },
    {
      id: "person-meera",
      name: "Meera Gupta",
      role: "Manager - People and Culture",
      city: "Mumbai",
      category: "people",
      initials: "MG",
      gradient: "cool",
      blurb: "Works across hiring, engagement and culture initiatives that deserve a home inside Connect.",
      teams: ["People", "Culture"],
      skills: ["Culture programming", "Onboarding", "Manager support"],
      availability: "Best for people experience ideas",
    },
  ],
  knowledgeItems: [
    {
      id: "resource-committee-checklist",
      title: "Rating committee checklist",
      category: "template",
      summary: "A pre-committee checklist for analysts to confirm note quality, missing questions and escalation points.",
      owner: "Ratings Office",
      updated: "Updated 3 days ago",
      format: "Checklist",
      savedByDefault: true,
    },
    {
      id: "resource-surveillance-template",
      title: "Surveillance note template",
      category: "template",
      summary: "A standard structure for surveillance notes so teams do not rebuild the same frame each time.",
      owner: "Corporate Ratings",
      updated: "Updated last week",
      format: "Template",
      savedByDefault: false,
    },
    {
      id: "resource-leave-policy",
      title: "Leave and travel policy FY26",
      category: "policy",
      summary: "Latest internal guidance for leave planning, travel approvals and reimbursement expectations.",
      owner: "HR Operations",
      updated: "Updated this month",
      format: "Policy",
      savedByDefault: false,
    },
    {
      id: "resource-writing-standards",
      title: "Research writing standards",
      category: "learning",
      summary: "A short guide to sharper structure, clearer narrative flow and more confident analytical writing.",
      owner: "Research Office",
      updated: "Updated 5 days ago",
      format: "Guide",
      savedByDefault: true,
    },
    {
      id: "resource-onboarding-playbook",
      title: "New joiner playbook",
      category: "learning",
      summary: "The first-stop playbook for new hires across tools, expectations, internal terms and common workflows.",
      owner: "People Team",
      updated: "Updated 2 weeks ago",
      format: "Playbook",
      savedByDefault: false,
    },
    {
      id: "resource-sector-archive",
      title: "Sector outlook archive",
      category: "research",
      summary: "A browsable list of published sector outlooks that should eventually surface directly in Connect search.",
      owner: "Research Office",
      updated: "Updated yesterday",
      format: "Archive",
      savedByDefault: false,
    },
    {
      id: "resource-townhall-pack",
      title: "Town hall deck archive",
      category: "research",
      summary: "A central home for internal decks, scorecards and business updates presented in town halls.",
      owner: "Internal Comms",
      updated: "Updated yesterday",
      format: "Deck library",
      savedByDefault: false,
    },
  ],
  workflows: [
    {
      id: "workflow-onboarding",
      title: "New joiner experience",
      description: "Connect people introductions, onboarding resources, mandatory policies and first-month check-ins.",
      stage: "Design",
      initials: "NJ",
      gradient: "cool",
    },
    {
      id: "workflow-helpdesk",
      title: "Help desk intake and triage",
      description: "Bring HR, IT and admin requests into a single routing layer with ownership and SLA visibility.",
      stage: "Next",
      initials: "HD",
      gradient: "warm",
    },
    {
      id: "workflow-policy",
      title: "Policy change acknowledgements",
      description: "Publish updates in Connect, collect acknowledgements and keep an audit trail.",
      stage: "Pilot candidate",
      initials: "PC",
      gradient: "gold",
    },
    {
      id: "workflow-spotlight",
      title: "Spotlight nominations",
      description: "Nominate colleagues from the feed, route approvals and publish weekly stories with less manual coordination.",
      stage: "Pilot candidate",
      initials: "SL",
      gradient: "fire",
    },
  ],
  birthdays: [
    { id: "birthday-sneha", name: "Sneha Patil", date: "Today!", initials: "SP", gradient: "cool", highlight: true },
    { id: "birthday-amit", name: "Amit Kumar", date: "Mar 24", initials: "AK", gradient: "warm", highlight: false },
    { id: "birthday-riya", name: "Riya Desai", date: "Mar 26", initials: "RD", gradient: "sun", highlight: false },
  ],
  anniversaries: [
    { id: "anniversary-priya", name: "Priya Sharma", date: "5 years", initials: "PS", gradient: "fire", highlight: true },
    { id: "anniversary-vikram", name: "Vikram Joshi", date: "3 yrs - Mar 25", initials: "VJ", gradient: "cool", highlight: false },
  ],
  upcoming: [
    { id: "event-townhall", date: "Mar 25", name: "Town Hall - Q4 Results" },
    { id: "event-finals", date: "Mar 28", name: "Cricket Finals" },
    { id: "event-holi", date: "Apr 2", name: "Holi Celebration" },
  ],
  pollOptions: [
    { id: "poll-directory", label: "People Directory", votes: 47, color: "rgba(247,148,29,0.12)" },
    { id: "poll-tools", label: "Tool Hub", votes: 34, color: "rgba(46,173,43,0.10)" },
    { id: "poll-knowledge", label: "Knowledge Hub", votes: 26, color: "rgba(255,199,44,0.12)" },
    { id: "poll-helpdesk", label: "Help Desk", votes: 20, color: "rgba(141,198,63,0.10)" },
  ],
};

const kudosTags = [
  { id: "analysis", label: "Sharp Analysis", className: "tag tag-analysis" },
  { id: "teamwork", label: "Team Player", className: "tag tag-teamwork" },
  { id: "client", label: "Client Hero", className: "tag tag-client" },
  { id: "mentor", label: "Mentored Me", className: "tag tag-mentor" },
  { id: "innovation", label: "Innovation", className: "tag tag-innovation" },
];

const defaultState = {
  theme: "",
  activeTab: "home",
  bulletinFilter: "all",
  pitchFilter: "trending",
  momentsFilter: "all",
  knowledgeFilter: "all",
  directoryFilter: "all",
  directoryQuery: "",
  selectedKudosTagId: "analysis",
  likedPostIds: [],
  joinedClubIds: appData.clubs.filter((club) => club.defaultJoined).map((club) => club.id),
  upvotedPitchIds: appData.pitches.filter((pitch) => pitch.defaultUpvoted).map((pitch) => pitch.id),
  bookmarkedKnowledgeIds: appData.knowledgeItems.filter((item) => item.savedByDefault).map((item) => item.id),
  pollVote: "",
  customBulletins: [],
  customKudos: [],
  customPitches: [],
};

let state = hydrateState();
let elements = {};
let latestSearchResults = [];
let toastTimeoutId = null;

document.addEventListener("DOMContentLoaded", () => {
  void init();
});

async function init() {
  const authenticatedUser = window.AcuiteConnectAuth && window.AcuiteConnectAuth.requireAuth
    ? await window.AcuiteConnectAuth.requireAuth({ loginPath: "/login.html" })
    : null;
  if (window.AcuiteConnectAuth && !authenticatedUser) {
    return;
  }
  if (authenticatedUser) {
    appData.currentUser = {
      ...appData.currentUser,
      ...authenticatedUser,
    };
  }

  elements = {
    searchInput: document.getElementById("global-search"),
    searchResults: document.getElementById("search-results"),
    directorySearchInput: document.getElementById("directory-search"),
    bulletinForm: document.getElementById("bulletin-form"),
    kudosForm: document.getElementById("kudos-form"),
    pitchForm: document.getElementById("pitch-form"),
    toast: document.getElementById("toast"),
    navAvatar: document.getElementById("nav-avatar"),
    composeAvatar: document.getElementById("compose-avatar"),
    profileAvatar: document.getElementById("profile-avatar"),
    profileName: document.getElementById("profile-name"),
    profileRole: document.getElementById("profile-role"),
    profileKudos: document.getElementById("profile-kudos"),
    profileClubs: document.getElementById("profile-clubs"),
    profilePitches: document.getElementById("profile-pitches"),
  };

  bindEvents();
  renderAll();
}

function bindEvents() {
  document.addEventListener("click", (event) => {
    void handleDocumentClick(event);
  });
  document.addEventListener("submit", handleSubmit);

  elements.searchInput.addEventListener("input", handleSearchInput);
  elements.searchInput.addEventListener("keydown", handleSearchKeydown);
  elements.searchInput.addEventListener("focus", () => {
    if (elements.searchInput.value.trim()) {
      updateSearchResults(elements.searchInput.value.trim());
    }
  });

  elements.directorySearchInput.addEventListener("input", (event) => {
    state.directoryQuery = event.target.value;
    saveState();
    renderDirectory();
  });
}

async function handleDocumentClick(event) {
  const searchResult = event.target.closest("[data-search-result]");
  if (searchResult) {
    const index = Number(searchResult.dataset.searchResult);
    const result = latestSearchResults[index];
    if (result) {
      useSearchResult(result);
    }
    return;
  }

  const action = event.target.closest("[data-action]");
  if (action) {
    const { action: actionName } = action.dataset;

    if (actionName === "toggle-theme") {
      toggleTheme();
      return;
    }

    if (actionName === "open-launcher") {
      switchTab("tools");
      showToast("Jumped to the Tool Hub.");
      return;
    }

    if (actionName === "logout") {
      if (window.AcuiteConnectAuth && window.AcuiteConnectAuth.logout) {
        await window.AcuiteConnectAuth.logout();
      }
      window.location.href = "/login.html";
      return;
    }

    if (actionName === "toggle-like") {
      state.likedPostIds = toggleArrayValue(state.likedPostIds, action.dataset.id);
      saveState();
      renderAll();
      return;
    }

    if (actionName === "celebrate") {
      showToast("Recognition noted. This is ready for a future reactions layer.");
      return;
    }

    if (actionName === "toggle-club") {
      state.joinedClubIds = toggleArrayValue(state.joinedClubIds, action.dataset.id);
      saveState();
      renderAll();
      return;
    }

    if (actionName === "toggle-pitch") {
      state.upvotedPitchIds = toggleArrayValue(state.upvotedPitchIds, action.dataset.id);
      saveState();
      renderAll();
      return;
    }

    if (actionName === "vote-poll") {
      state.pollVote = action.dataset.id;
      saveState();
      renderPoll();
      return;
    }

    if (actionName === "open-tool") {
      openTool(action.dataset.id);
      return;
    }

    if (actionName === "select-kudos-tag") {
      state.selectedKudosTagId = action.dataset.id;
      saveState();
      renderKudosTags();
      return;
    }

    if (actionName === "toggle-bookmark") {
      state.bookmarkedKnowledgeIds = toggleArrayValue(state.bookmarkedKnowledgeIds, action.dataset.id);
      saveState();
      renderKnowledge();
      renderSavedResources();
      return;
    }

    if (actionName === "jump-to-item") {
      jumpToItem(action.dataset.tab, action.dataset.targetId);
      return;
    }

    if (actionName === "nominate-spotlight") {
      showToast("Spotlight nomination can be the next workflow we wire into Connect.");
      return;
    }

    if (actionName === "invite-alumni") {
      showToast("Alumni invitations are staged as a future step for this MVP.");
      return;
    }

    if (actionName === "show-person") {
      showToast(`Expertise profile for ${action.dataset.name} can open from here in the next iteration.`);
      return;
    }

    if (actionName === "preview-resource") {
      showToast(`Preview for "${action.dataset.name}" is ready to connect to a real document link.`);
      return;
    }

    if (actionName === "post-cta") {
      if (action.dataset.tab) {
        switchTab(action.dataset.tab);
      }
      showToast(action.dataset.message || "Action captured.");
      return;
    }

    if (actionName === "placeholder-comment") {
      showToast("Comments can be attached once the backend layer is in place.");
      return;
    }

    if (actionName === "connect-alumni") {
      showToast(`Connection request for ${action.dataset.name} can be routed from here later.`);
      return;
    }
  }

  const switcher = event.target.closest("[data-switch-tab]");
  if (switcher) {
    switchTab(switcher.dataset.switchTab);
    return;
  }

  const filterButton = event.target.closest(".filter-tabs button");
  if (filterButton) {
    const group = filterButton.closest("[data-filter-group]")?.dataset.filterGroup;
    if (group) {
      setFilter(group, filterButton.dataset.filter);
    }
    return;
  }

  const directoryChip = event.target.closest("[data-directory-filter]");
  if (directoryChip) {
    state.directoryFilter = directoryChip.dataset.directoryFilter;
    saveState();
    renderDirectory();
    renderDirectoryChips();
    return;
  }

  if (!event.target.closest(".topnav-search")) {
    hideSearchResults();
  }
}

function handleSubmit(event) {
  if (event.target === elements.bulletinForm) {
    event.preventDefault();
    submitBulletin();
    return;
  }

  if (event.target === elements.kudosForm) {
    event.preventDefault();
    submitKudos();
    return;
  }

  if (event.target === elements.pitchForm) {
    event.preventDefault();
    submitPitch();
  }
}

function handleSearchInput(event) {
  updateSearchResults(event.target.value.trim());
}

function handleSearchKeydown(event) {
  if (event.key === "Enter" && latestSearchResults.length) {
    event.preventDefault();
    useSearchResult(latestSearchResults[0]);
  }
}

function renderAll() {
  applyTheme();
  renderPanels();
  renderProfile();
  renderHeroStats();
  renderTodayPanel();
  renderTasksPanel();
  renderPulsePanel();
  renderHomeTools();
  renderHomeFeed();
  renderBulletinFeed();
  renderKudosTags();
  renderWallFeed();
  renderLeaderboard();
  renderClubs();
  renderSpotlight();
  renderPitches();
  renderMoments();
  renderAlumni();
  renderDirectoryChips();
  renderDirectory();
  renderToolSummary();
  renderToolGrid();
  renderWorkflows();
  renderKnowledge();
  renderBirthdays();
  renderAnniversaries();
  renderUpcoming();
  renderPoll();
  renderSavedResources();
  syncFilterButtons();
}

function renderPanels() {
  document.documentElement.setAttribute("data-theme", state.theme);
  document.querySelectorAll(".panel").forEach((panel) => {
    panel.classList.toggle("active", panel.id === `panel-${state.activeTab}`);
  });
  document.querySelectorAll(".sidebar-left .tab").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.switchTab === state.activeTab);
  });
}

function renderProfile() {
  const receivedKudos = 12 + state.customKudos.filter((item) => item.recipient.toLowerCase() === appData.currentUser.name.toLowerCase()).length;
  const joinedClubs = state.joinedClubIds.length;
  const pitchesByRahul = appData.pitches.filter((item) => item.author === appData.currentUser.name).length + state.customPitches.length;

  elements.navAvatar.textContent = appData.currentUser.initials;
  if (elements.composeAvatar) {
    elements.composeAvatar.textContent = appData.currentUser.initials;
  }
  elements.profileAvatar.textContent = appData.currentUser.initials;
  elements.profileName.textContent = appData.currentUser.name;
  elements.profileRole.textContent = appData.currentUser.role;
  elements.profileKudos.textContent = String(receivedKudos);
  elements.profileClubs.textContent = String(joinedClubs);
  elements.profilePitches.textContent = String(pitchesByRahul);
}

function renderHeroStats() {
  const stats = [
    {
      label: "People directory",
      value: String(appData.directory.length),
      note: "Profiles mapped by expertise and city",
    },
    {
      label: "Tools in scope",
      value: String(appData.quickTools.length),
      note: "Live, pilot and planned workflow surfaces",
    },
    {
      label: "Knowledge items",
      value: String(appData.knowledgeItems.length),
      note: "Policies, templates and learning resources",
    },
  ];

  document.getElementById("hero-stats").innerHTML = stats.map((item) => `
    <article class="hero-stat">
      <div class="hero-stat-label">${escapeHtml(item.label)}</div>
      <div class="hero-stat-value">${escapeHtml(item.value)}</div>
      <div class="hero-stat-note">${escapeHtml(item.note)}</div>
    </article>
  `).join("");
}

function renderTodayPanel() {
  document.getElementById("today-panel").innerHTML = `
    <p class="widget-kicker">Today</p>
    <h3>My day</h3>
    <p class="muted-copy">A lightweight look at the day without leaving the feed.</p>
    <ul class="mini-list">
      ${appData.agenda.map((item) => `
        <li>
          <div>
            <div class="mini-item-title">${escapeHtml(item.title)}</div>
            <div class="mini-item-meta">${escapeHtml(item.meta)}</div>
          </div>
          <div class="mini-item-time">${escapeHtml(item.time)}</div>
        </li>
      `).join("")}
    </ul>
  `;
}

function renderTasksPanel() {
  document.getElementById("tasks-panel").innerHTML = `
    <p class="widget-kicker">Action queue</p>
    <h3>What needs attention</h3>
    <p class="muted-copy">A simple bridge between culture and work actions.</p>
    <ul class="mini-list">
      ${appData.tasks.map((item) => `
        <li>
          <div>
            <div class="mini-item-title">${escapeHtml(item.title)}</div>
            <div class="mini-item-meta">${escapeHtml(item.due)}</div>
          </div>
          <span class="task-badge ${escapeHtml(item.priority)}">${escapeHtml(item.priority)}</span>
        </li>
      `).join("")}
    </ul>
  `;
}

function renderPulsePanel() {
  document.getElementById("pulse-panel").innerHTML = `
    <p class="widget-kicker">Pulse</p>
    <h3>Connect snapshot</h3>
    <p class="muted-copy">Useful signs that the platform is becoming more than a social feed.</p>
    <div class="pulse-grid">
      ${appData.pulse.map((item) => `
        <article class="pulse-card">
          <strong>${escapeHtml(item.value)}</strong>
          <span>${escapeHtml(item.label)}</span>
        </article>
      `).join("")}
    </div>
  `;
}

function renderHomeTools() {
  document.getElementById("home-tools-grid").innerHTML = appData.quickTools.slice(0, 4).map(renderToolCard).join("");
}

function renderHomeFeed() {
  const homeFeed = [
    ...state.customBulletins.slice(0, 1).map(mapCustomBulletinToPost),
    ...state.customKudos.slice(0, 1).map(mapCustomKudosToPost),
    ...appData.homePosts,
  ];
  document.getElementById("home-feed").innerHTML = homeFeed.map(renderPost).join("");
}

function renderBulletinFeed() {
  const allPosts = [...state.customBulletins.map(mapCustomBulletinToPost), ...appData.bulletinPosts];
  const filtered = allPosts.filter((post) => state.bulletinFilter === "all" || post.category === state.bulletinFilter);
  document.getElementById("bulletin-feed").innerHTML = filtered.length
    ? filtered.map(renderPost).join("")
    : `<div class="empty-state">No bulletin posts match this filter yet.</div>`;
}

function renderKudosTags() {
  document.getElementById("kudos-tags").innerHTML = kudosTags.map((tag) => `
    <button
      type="button"
      class="${tag.className} ${state.selectedKudosTagId === tag.id ? "active" : ""}"
      data-action="select-kudos-tag"
      data-id="${tag.id}"
    >
      ${escapeHtml(tag.label)}
    </button>
  `).join("");
}

function renderWallFeed() {
  const posts = [...state.customKudos.map(mapCustomKudosToPost), ...appData.wallPosts];
  document.getElementById("wall-feed").innerHTML = posts.map(renderKudosPost).join("");
}

function renderLeaderboard() {
  document.getElementById("leaderboard-card").innerHTML = `
    <p class="widget-kicker">Recognition</p>
    <h3>Most appreciated this month</h3>
    <ul class="mini-list">
      ${appData.leaderboard.map((person) => `
        <li>
          <div>
            <div class="mini-item-title">${escapeHtml(person.name)}</div>
            <div class="mini-item-meta">Recognition posts received</div>
          </div>
          <div class="mini-item-time">${escapeHtml(String(person.count))}</div>
        </li>
      `).join("")}
    </ul>
  `;
}

function renderClubs() {
  document.getElementById("clubs-grid").innerHTML = appData.clubs.map((club) => {
    const joined = state.joinedClubIds.includes(club.id);
    const members = club.members + (joined && !club.defaultJoined ? 1 : 0) - (!joined && club.defaultJoined ? 1 : 0);
    return `
      <article class="club-card" id="${club.id}">
        <div class="club-banner" style="background:${club.background}">
          <div class="club-emoji">${club.emoji}</div>
        </div>
        <div class="club-card-body">
          <h3>${escapeHtml(club.name)}</h3>
          <p>${escapeHtml(club.description)}</p>
          <div class="mini-item-meta">${escapeHtml(club.nextEvent)}</div>
          <div class="club-members">
            <div class="avatars">
              ${club.avatars.map((avatar) => `
                <div class="mini-av" style="background:${gradientValue(avatar.gradient)}">${escapeHtml(avatar.initials)}</div>
              `).join("")}
            </div>
            <span class="count">${escapeHtml(String(members))}</span>
            <button
              type="button"
              class="club-join ${joined ? "joined" : ""}"
              data-action="toggle-club"
              data-id="${club.id}"
            >
              ${joined ? "Joined" : "Join"}
            </button>
          </div>
        </div>
      </article>
    `;
  }).join("");
}

function renderSpotlight() {
  const current = appData.spotlights[0];
  document.getElementById("spotlight-feature").innerHTML = `
    <article class="spotlight-feature" id="${current.id}">
      <div class="spotlight-photo">
        <div class="big-avatar">${escapeHtml(current.initials)}</div>
      </div>
      <div class="spotlight-content">
        <div class="eyebrow">This week</div>
        <h2>${escapeHtml(current.name)}</h2>
        <div class="spotlight-role">${escapeHtml(current.role)}</div>
        <div class="spotlight-qa">
          ${current.qa.map((item) => `
            <div>
              <div class="q">${escapeHtml(item.question)}</div>
              <div class="a">${escapeHtml(item.answer)}</div>
            </div>
          `).join("")}
        </div>
      </div>
    </article>
  `;

  document.getElementById("previous-spotlights").innerHTML = appData.spotlights.slice(1).map((person) => `
    <article class="prev-spot">
      <div class="card-avatar" style="width:56px;height:56px;font-size:20px;margin:0 auto 10px;background:${gradientValue(person.photoGradient)};border-radius:50%">
        ${escapeHtml(person.initials)}
      </div>
      <div style="font-size:15px;font-weight:700">${escapeHtml(person.name)}</div>
      <div style="font-size:12px;color:var(--text3)">${escapeHtml(person.role)}</div>
    </article>
  `).join("");
}

function renderPitches() {
  const base = [...state.customPitches.map(mapCustomPitchToPost), ...appData.pitches];
  let pitches = base.slice();

  if (state.pitchFilter === "done") {
    pitches = pitches.filter((item) => item.status === "approved" || item.status === "implemented");
  } else if (state.pitchFilter === "new") {
    pitches.sort((left, right) => right.createdAt - left.createdAt);
  } else {
    pitches.sort((left, right) => getPitchVotes(right) - getPitchVotes(left));
  }

  document.getElementById("pitch-list").innerHTML = pitches.length
    ? pitches.map(renderPitchCard).join("")
    : `<div class="empty-state">No ideas are in this bucket yet.</div>`;
}

function renderMoments() {
  const items = appData.moments.filter((moment) => state.momentsFilter === "all" || moment.category === state.momentsFilter);
  document.getElementById("moments-grid").innerHTML = items.map((moment) => `
    <article class="moment-item" id="${moment.id}" style="background:${moment.background}">
      <div class="moment-placeholder">${moment.emoji}</div>
      <div class="overlay">
        <p>${escapeHtml(moment.title)}</p>
        <span>${escapeHtml(String(moment.photos))} photos</span>
      </div>
    </article>
  `).join("");
}

function renderAlumni() {
  document.getElementById("alumni-grid").innerHTML = appData.alumni.map((person) => `
    <article class="alumni-card" id="${person.id}">
      <div class="alumni-avatar" style="background:${gradientValue(person.gradient)}">${escapeHtml(person.initials)}</div>
      <h4>${escapeHtml(person.name)}</h4>
      <div class="alumni-current">${escapeHtml(person.current)}</div>
      <div class="alumni-badge">${escapeHtml(person.batch)}</div>
      <div class="alumni-tenure">${escapeHtml(person.tenure)}</div>
      <button type="button" class="connect-btn" data-action="connect-alumni" data-name="${escapeHtml(person.name)}">Connect</button>
    </article>
  `).join("");
}

function renderDirectoryChips() {
  const chips = [
    { id: "all", label: "All" },
    { id: "ratings", label: "Ratings" },
    { id: "research", label: "Research" },
    { id: "ops", label: "Operations" },
    { id: "people", label: "People" },
  ];

  document.getElementById("directory-chips").innerHTML = chips.map((chip) => `
    <button
      type="button"
      class="${state.directoryFilter === chip.id ? "active" : ""}"
      data-directory-filter="${chip.id}"
    >
      ${escapeHtml(chip.label)}
    </button>
  `).join("");
}

function renderDirectory() {
  elements.directorySearchInput.value = state.directoryQuery;
  const query = state.directoryQuery.trim().toLowerCase();
  const filtered = appData.directory.filter((person) => {
    const matchesCategory = state.directoryFilter === "all" || person.category === state.directoryFilter;
    if (!matchesCategory) {
      return false;
    }

    if (!query) {
      return true;
    }

    const haystack = [
      person.name,
      person.role,
      person.city,
      person.blurb,
      person.teams.join(" "),
      person.skills.join(" "),
    ].join(" ").toLowerCase();

    return haystack.includes(query);
  });

  document.getElementById("directory-grid").innerHTML = filtered.length
    ? filtered.map((person) => `
      <article class="person-card" id="${person.id}">
        <div class="person-head">
          <div class="person-avatar" style="background:${gradientValue(person.gradient)}">${escapeHtml(person.initials)}</div>
          <div class="person-meta">
            <h3>${escapeHtml(person.name)}</h3>
            <div class="person-role">${escapeHtml(person.role)}</div>
            <div class="person-location">${escapeHtml(person.city)}</div>
          </div>
        </div>
        <p>${escapeHtml(person.blurb)}</p>
        <div class="team-row">
          ${person.teams.map((team) => `<span class="team-chip">${escapeHtml(team)}</span>`).join("")}
        </div>
        <div class="skill-row">
          ${person.skills.map((skill) => `<span class="skill-chip">${escapeHtml(skill)}</span>`).join("")}
        </div>
        <div class="person-footer">
          <span class="availability">${escapeHtml(person.availability)}</span>
          <button type="button" class="btn-outline" data-action="show-person" data-name="${escapeHtml(person.name)}">View expertise</button>
        </div>
      </article>
    `).join("")
    : `<div class="empty-state">No people matched that filter. Try a broader team or skill search.</div>`;
}

function renderToolSummary() {
  const liveTools = appData.quickTools.filter((tool) => tool.status === "live").length;
  const pilotTools = appData.quickTools.filter((tool) => tool.status === "pilot").length;
  const savedResources = state.bookmarkedKnowledgeIds.length;

  const summary = [
    { value: String(liveTools), label: "Live tools", note: "Ready to connect now" },
    { value: String(pilotTools), label: "Pilot modules", note: "Good next wave for rollout" },
    { value: String(savedResources), label: "Saved resources", note: "Personal quick-access shelf" },
  ];

  document.getElementById("tool-summary-grid").innerHTML = summary.map((item) => `
    <article class="summary-card">
      <strong>${escapeHtml(item.value)}</strong>
      <span>${escapeHtml(item.label)}</span>
      <p>${escapeHtml(item.note)}</p>
    </article>
  `).join("");
}

function renderToolGrid() {
  document.getElementById("tool-grid").innerHTML = appData.quickTools.map(renderToolCard).join("");
}

function renderWorkflows() {
  document.getElementById("workflow-list").innerHTML = appData.workflows.map((workflow) => `
    <article class="workflow-item" id="${workflow.id}">
      <div class="workflow-icon" style="background:${gradientValue(workflow.gradient)}">${escapeHtml(workflow.initials)}</div>
      <div class="workflow-body">
        <h4>${escapeHtml(workflow.title)}</h4>
        <p>${escapeHtml(workflow.description)}</p>
      </div>
      <div class="workflow-stage">${escapeHtml(workflow.stage)}</div>
    </article>
  `).join("");
}

function renderKnowledge() {
  const filtered = appData.knowledgeItems.filter((item) => state.knowledgeFilter === "all" || item.category === state.knowledgeFilter);
  document.getElementById("knowledge-list").innerHTML = filtered.length
    ? filtered.map((item) => {
      const saved = state.bookmarkedKnowledgeIds.includes(item.id);
      return `
        <article class="resource-card" id="${item.id}">
          <div class="resource-card-head">
            <span class="resource-badge ${escapeHtml(item.category)}">${escapeHtml(capitalize(item.category))}</span>
            <button
              type="button"
              class="resource-bookmark ${saved ? "saved" : ""}"
              data-action="toggle-bookmark"
              data-id="${item.id}"
            >
              ${saved ? "Saved" : "Save"}
            </button>
          </div>
          <div class="resource-title">${escapeHtml(item.title)}</div>
          <p>${escapeHtml(item.summary)}</p>
          <div class="resource-meta">
            <span>Owner: ${escapeHtml(item.owner)}</span>
            <span>${escapeHtml(item.updated)}</span>
            <span>${escapeHtml(item.format)}</span>
          </div>
          <div class="card-actions">
            <button
              type="button"
              class="action-btn"
              data-action="preview-resource"
              data-name="${escapeHtml(item.title)}"
            >
              Preview
            </button>
            <div class="spacer"></div>
          </div>
        </article>
      `;
    }).join("")
    : `<div class="empty-state">No resources match this filter yet.</div>`;

  document.getElementById("knowledge-saved-list").innerHTML = renderSavedResourceLinks("knowledge");
}

function renderBirthdays() {
  document.getElementById("birthdays-list").innerHTML = appData.birthdays.map((person) => `
    <div class="bday-item">
      <div class="bday-avatar" style="background:${gradientValue(person.gradient)}">${escapeHtml(person.initials)}</div>
      <div class="bday-info">
        <div class="name">${escapeHtml(person.name)}</div>
        <div class="date ${person.highlight ? "today" : ""}">${escapeHtml(person.date)}</div>
      </div>
    </div>
  `).join("");
}

function renderAnniversaries() {
  document.getElementById("anniversaries-list").innerHTML = appData.anniversaries.map((person) => `
    <div class="bday-item">
      <div class="bday-avatar" style="background:${gradientValue(person.gradient)}">${escapeHtml(person.initials)}</div>
      <div class="bday-info">
        <div class="name">${escapeHtml(person.name)}</div>
        <div class="date ${person.highlight ? "today" : ""}">${escapeHtml(person.date)}</div>
      </div>
    </div>
  `).join("");
}

function renderUpcoming() {
  document.getElementById("upcoming-events").innerHTML = appData.upcoming.map((item) => `
    <div class="event-item">
      <div class="event-date">${escapeHtml(item.date)}</div>
      <div class="event-name">${escapeHtml(item.name)}</div>
    </div>
  `).join("");
}

function renderPoll() {
  const totals = appData.pollOptions.reduce((sum, option) => sum + option.votes, 0) + (state.pollVote ? 1 : 0);
  document.getElementById("poll-list").innerHTML = appData.pollOptions.map((option) => {
    const votes = option.votes + (state.pollVote === option.id ? 1 : 0);
    const pct = Math.round((votes / totals) * 100);
    const voted = state.pollVote === option.id;
    return `
      <button
        type="button"
        class="poll-option ${voted ? "voted" : ""}"
        data-action="vote-poll"
        data-id="${option.id}"
      >
        <div class="poll-bar" style="width:${pct}%;background:${option.color}"></div>
        <span class="poll-text">${escapeHtml(option.label)}</span>
        <span class="poll-pct">${escapeHtml(String(pct))}%</span>
      </button>
    `;
  }).join("");
}

function renderSavedResources() {
  document.getElementById("saved-resources").innerHTML = renderSavedResourceLinks("sidebar");
}

function renderSavedResourceLinks(scope) {
  const savedItems = appData.knowledgeItems.filter((item) => state.bookmarkedKnowledgeIds.includes(item.id));
  if (!savedItems.length) {
    return `<div class="empty-state">${scope === "sidebar" ? "Save a resource to keep it close in the sidebar." : "Saved items will appear here."}</div>`;
  }

  return savedItems.map((item) => `
    <button
      type="button"
      class="saved-link"
      data-action="jump-to-item"
      data-tab="knowledge"
      data-target-id="${item.id}"
    >
      <strong>${escapeHtml(item.title)}</strong>
      <span>${escapeHtml(capitalize(item.category))} - ${escapeHtml(item.owner)}</span>
    </button>
  `).join("");
}

function renderToolCard(tool) {
  const buttonLabel = tool.url ? "Open" : tool.tab ? "Explore" : "Preview";
  return `
    <article class="tool-card" id="${tool.id}">
      <div class="tool-card-head">
        <div class="tool-icon" style="background:${gradientValue(tool.gradient)}">${escapeHtml(tool.initials)}</div>
        <div>
          <h3>${escapeHtml(tool.name)}</h3>
          <span class="tool-status ${tool.status}">${escapeHtml(capitalize(tool.status))}</span>
        </div>
      </div>
      <p>${escapeHtml(tool.summary)}</p>
      <div class="tool-meta">
        <span class="mini-item-meta">${escapeHtml(tool.note)}</span>
        <button
          type="button"
          class="tool-open ${tool.status === "live" ? "live" : ""}"
          data-action="open-tool"
          data-id="${tool.id}"
        >
          ${escapeHtml(buttonLabel)}
        </button>
      </div>
    </article>
  `;
}

function renderPost(post) {
  return post.kind === "kudos" ? renderKudosPost(post) : renderStandardPost(post);
}

function renderStandardPost(post) {
  const liked = state.likedPostIds.includes(post.id);
  const classes = [
    "card",
    post.variant === "pinned" ? "pinned" : "",
    post.variant === "welcome" ? "welcome" : "",
    post.variant === "milestone" ? "milestone" : "",
  ].filter(Boolean).join(" ");

  return `
    <article class="${classes}" id="${post.id}">
      <div class="card-header">
        <div class="card-avatar" style="background:${gradientValue(post.avatar)}">${escapeHtml(post.initials)}</div>
        <div class="card-meta">
          <div class="card-name">${escapeHtml(post.authorName)}</div>
          <div class="card-sub">${escapeHtml(post.authorMeta)}</div>
        </div>
        ${post.variant === "pinned" ? `<div style="margin-left:auto"><span class="pin-badge">Pinned</span></div>` : ""}
      </div>
      <div class="card-body">
        <div class="card-title">${escapeHtml(post.title)}</div>
        ${post.body.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("")}
      </div>
      <div class="card-actions">
        <button type="button" class="action-btn ${liked ? "liked" : ""}" data-action="toggle-like" data-id="${post.id}">
          ${likeIcon()}${escapeHtml(String(getPostLikeCount(post)))}
        </button>
        ${typeof post.comments === "number" ? `
          <button type="button" class="action-btn" data-action="placeholder-comment">
            ${commentIcon()}${escapeHtml(String(post.comments))}
          </button>
        ` : ""}
        <div class="spacer"></div>
        ${post.actionLabel ? `
          <button
            type="button"
            class="action-btn"
            data-action="post-cta"
            data-tab="${post.actionTab || ""}"
            data-message="${escapeHtml(post.actionMessage || `Opened ${post.actionLabel.toLowerCase()}.`)}"
          >
            ${escapeHtml(post.actionLabel)}
          </button>
        ` : ""}
      </div>
      ${typeof post.comments === "number" ? `
        <div class="comment-box">
          <div class="avatar" style="width:28px;height:28px;font-size:10px">${escapeHtml(appData.currentUser.initials)}</div>
          <input type="text" placeholder="Write a comment..." aria-label="Comment">
          <button type="button" class="comment-submit" data-action="placeholder-comment">Post</button>
        </div>
      ` : ""}
    </article>
  `;
}

function renderKudosPost(post) {
  const liked = state.likedPostIds.includes(post.id);
  const tag = kudosTags.find((item) => item.id === post.tagId) || kudosTags[0];
  return `
    <article class="card kudos-card" id="${post.id}">
      <div class="kudos-header">
        <strong>${escapeHtml(post.giver)}</strong>
        <span>to</span>
        <strong>${escapeHtml(post.recipient)}</strong>
        <span class="${tag.className}">${escapeHtml(tag.label)}</span>
      </div>
      <div class="kudos-quote">"${escapeHtml(post.message)}"</div>
      <div class="kudos-recipient">
        <div class="card-avatar" style="background:${gradientValue(post.avatar)};width:38px;height:38px;font-size:13px;border-radius:12px">
          ${escapeHtml(post.initials)}
        </div>
        <div>
          <div class="name">${escapeHtml(post.recipient)}</div>
          <div class="role">${escapeHtml(post.recipientRole)}</div>
        </div>
      </div>
      <div class="card-actions">
        <button type="button" class="action-btn ${liked ? "liked" : ""}" data-action="toggle-like" data-id="${post.id}">
          ${likeIcon()}${escapeHtml(String(getPostLikeCount(post)))}
        </button>
        <button type="button" class="action-btn" data-action="celebrate">Celebrate</button>
      </div>
    </article>
  `;
}

function renderPitchCard(pitch) {
  const upvoted = state.upvotedPitchIds.includes(pitch.id);
  return `
    <article class="pitch-card" id="${pitch.id}">
      <div class="pitch-vote">
        <button type="button" class="${upvoted ? "upvoted" : ""}" data-action="toggle-pitch" data-id="${pitch.id}">
          ${upvoteIcon()}
        </button>
        <div class="count">${escapeHtml(String(getPitchVotes(pitch)))}</div>
      </div>
      <div class="pitch-body">
        <h4>${escapeHtml(pitch.title)}</h4>
        <p>${escapeHtml(pitch.description)}</p>
        <div class="pitch-meta">
          <span>By <strong>${escapeHtml(pitch.author)}</strong></span>
          <span>${escapeHtml(String(pitch.comments))} comments</span>
          <span class="pitch-status ${pitch.status}">${escapeHtml(statusLabel(pitch.status))}</span>
        </div>
      </div>
    </article>
  `;
}

function submitBulletin() {
  const formData = new FormData(elements.bulletinForm);
  const title = String(formData.get("title") || "").trim();
  const message = String(formData.get("message") || "").trim();
  const category = String(formData.get("category") || "announcements");

  if (!title || !message) {
    showToast("Add both a title and message before posting.");
    return;
  }

  state.customBulletins.unshift({
    id: `custom-bulletin-${Date.now()}`,
    title,
    message,
    category,
    likes: 0,
    comments: 0,
    createdAt: Date.now(),
  });
  saveState();
  elements.bulletinForm.reset();
  renderAll();
  showToast("Bulletin post added to the prototype.");
}

function submitKudos() {
  const formData = new FormData(elements.kudosForm);
  const recipient = String(formData.get("recipient") || "").trim();
  const message = String(formData.get("message") || "").trim();

  if (!recipient || !message) {
    showToast("Add both a recipient and a message before posting kudos.");
    return;
  }

  state.customKudos.unshift({
    id: `custom-kudos-${Date.now()}`,
    giver: appData.currentUser.name,
    recipient,
    recipientRole: "Colleague - Acuité",
    tagId: state.selectedKudosTagId,
    message,
    likes: 0,
    createdAt: Date.now(),
  });
  saveState();
  elements.kudosForm.reset();
  renderAll();
  showToast("Kudos posted to The Wall.");
}

function submitPitch() {
  const formData = new FormData(elements.pitchForm);
  const title = String(formData.get("title") || "").trim();
  const description = String(formData.get("description") || "").trim();
  const impact = String(formData.get("impact") || "people");

  if (!title || !description) {
    showToast("Add both an idea title and description before submitting.");
    return;
  }

  state.customPitches.unshift({
    id: `custom-pitch-${Date.now()}`,
    title,
    description: `${description} Impact area: ${capitalize(impact)}.`,
    author: appData.currentUser.name,
    comments: 0,
    status: "submitted",
    votes: 0,
    defaultUpvoted: false,
    createdAt: Date.now(),
  });
  saveState();
  elements.pitchForm.reset();
  renderAll();
  showToast("Idea submitted to The Pitch.");
}

function updateSearchResults(query) {
  if (!query) {
    latestSearchResults = [];
    hideSearchResults();
    return;
  }

  const lowerQuery = query.toLowerCase();
  latestSearchResults = buildSearchIndex()
    .filter((item) => item.searchText.includes(lowerQuery))
    .sort((left, right) => scoreSearchItem(left, lowerQuery) - scoreSearchItem(right, lowerQuery))
    .slice(0, 7);

  elements.searchResults.hidden = false;
  elements.searchResults.innerHTML = latestSearchResults.length
    ? latestSearchResults.map((result, index) => `
      <button type="button" class="search-result" data-search-result="${index}">
        <div>
          <div class="search-result-title">${escapeHtml(result.title)}</div>
          <div class="search-result-subtitle">${escapeHtml(result.subtitle)}</div>
        </div>
        <span class="search-result-type">${escapeHtml(result.type)}</span>
      </button>
    `).join("")
    : `<div class="search-empty">No matches yet. Try a person, tool, post title or resource.</div>`;
}

function hideSearchResults() {
  elements.searchResults.hidden = true;
}

function useSearchResult(result) {
  elements.searchInput.value = result.title;
  hideSearchResults();
  jumpToItem(result.tab, result.targetId);
}

function jumpToItem(tab, targetId) {
  switchTab(tab);
  window.requestAnimationFrame(() => {
    const target = document.getElementById(targetId);
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "center" });
      target.classList.add("flash-highlight");
      window.setTimeout(() => target.classList.remove("flash-highlight"), 1600);
    }
  });
}

function buildSearchIndex() {
  const bulletin = [...state.customBulletins.map(mapCustomBulletinToPost), ...appData.bulletinPosts].map((post) => ({
    title: post.title,
    subtitle: `${post.authorName} - Bulletin`,
    type: "post",
    tab: "bulletin",
    targetId: post.id,
    searchText: [post.title, post.authorName, post.body.join(" "), post.category].join(" ").toLowerCase(),
  }));

  const directory = appData.directory.map((person) => ({
    title: person.name,
    subtitle: `${person.role} - ${person.city}`,
    type: "person",
    tab: "directory",
    targetId: person.id,
    searchText: [person.name, person.role, person.city, person.skills.join(" "), person.teams.join(" "), person.blurb].join(" ").toLowerCase(),
  }));

  const tools = appData.quickTools.map((tool) => ({
    title: tool.name,
    subtitle: tool.summary,
    type: "tool",
    tab: "tools",
    targetId: tool.id,
    searchText: [tool.name, tool.summary, tool.note].join(" ").toLowerCase(),
  }));

  const resources = appData.knowledgeItems.map((item) => ({
    title: item.title,
    subtitle: `${capitalize(item.category)} - ${item.owner}`,
    type: "resource",
    tab: "knowledge",
    targetId: item.id,
    searchText: [item.title, item.summary, item.owner, item.category].join(" ").toLowerCase(),
  }));

  return [...bulletin, ...directory, ...tools, ...resources];
}

function scoreSearchItem(item, query) {
  const title = item.title.toLowerCase();
  if (title.startsWith(query)) {
    return 0;
  }
  if (title.includes(query)) {
    return 1;
  }
  if (item.searchText.includes(query)) {
    return 2;
  }
  return 3;
}

function openTool(toolId) {
  const tool = appData.quickTools.find((item) => item.id === toolId);
  if (!tool) {
    return;
  }

  if (tool.url) {
    window.open(tool.url, "_blank", "noopener");
    showToast(`Opening ${tool.name}.`);
    return;
  }

  if (tool.tab) {
    switchTab(tool.tab);
    showToast(`Jumped to ${tool.name}.`);
    return;
  }

  showToast(tool.message || `${tool.name} is queued for a later rollout.`);
}

function switchTab(tabId) {
  state.activeTab = tabId;
  saveState();
  hideSearchResults();
  renderPanels();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function setFilter(group, value) {
  if (group === "bulletin") {
    state.bulletinFilter = value;
    saveState();
    renderBulletinFeed();
    syncFilterButtons();
    return;
  }

  if (group === "pitch") {
    state.pitchFilter = value;
    saveState();
    renderPitches();
    syncFilterButtons();
    return;
  }

  if (group === "moments") {
    state.momentsFilter = value;
    saveState();
    renderMoments();
    syncFilterButtons();
    return;
  }

  if (group === "knowledge") {
    state.knowledgeFilter = value;
    saveState();
    renderKnowledge();
    syncFilterButtons();
  }
}

function syncFilterButtons() {
  const filterMap = {
    bulletin: state.bulletinFilter,
    pitch: state.pitchFilter,
    moments: state.momentsFilter,
    knowledge: state.knowledgeFilter,
  };

  document.querySelectorAll("[data-filter-group]").forEach((group) => {
    const groupName = group.dataset.filterGroup;
    const activeValue = filterMap[groupName];
    group.querySelectorAll("button").forEach((button) => {
      button.classList.toggle("active", button.dataset.filter === activeValue);
    });
  });
}

function toggleTheme() {
  state.theme = state.theme === "dark" ? "" : "dark";
  saveState();
  renderPanels();
}

function applyTheme() {
  document.documentElement.setAttribute("data-theme", state.theme);
}

function getPostLikeCount(post) {
  return post.likes + (state.likedPostIds.includes(post.id) ? 1 : 0);
}

function getPitchVotes(pitch) {
  return pitch.votes + (state.upvotedPitchIds.includes(pitch.id) && !pitch.defaultUpvoted ? 1 : 0) - (!state.upvotedPitchIds.includes(pitch.id) && pitch.defaultUpvoted ? 1 : 0);
}

function mapCustomBulletinToPost(item) {
  return {
    id: item.id,
    kind: "standard",
    variant: "default",
    category: item.category,
    title: item.title,
    body: [item.message],
    authorName: appData.currentUser.name,
    authorMeta: "Just now",
    initials: appData.currentUser.initials,
    avatar: "warm",
    likes: item.likes,
    comments: item.comments,
  };
}

function mapCustomKudosToPost(item) {
  return {
    id: item.id,
    kind: "kudos",
    giver: item.giver,
    recipient: item.recipient,
    recipientRole: item.recipientRole,
    tagId: item.tagId,
    message: item.message,
    initials: initialsFromName(item.recipient),
    avatar: "warm",
    likes: item.likes,
  };
}

function mapCustomPitchToPost(item) {
  return {
    ...item,
  };
}

function hydrateState() {
  const saved = readState();
  if (!saved) {
    return { ...defaultState };
  }

  return {
    ...defaultState,
    ...saved,
    likedPostIds: Array.isArray(saved.likedPostIds) ? saved.likedPostIds : defaultState.likedPostIds.slice(),
    joinedClubIds: Array.isArray(saved.joinedClubIds) ? saved.joinedClubIds : defaultState.joinedClubIds.slice(),
    upvotedPitchIds: Array.isArray(saved.upvotedPitchIds) ? saved.upvotedPitchIds : defaultState.upvotedPitchIds.slice(),
    bookmarkedKnowledgeIds: Array.isArray(saved.bookmarkedKnowledgeIds) ? saved.bookmarkedKnowledgeIds : defaultState.bookmarkedKnowledgeIds.slice(),
    customBulletins: Array.isArray(saved.customBulletins) ? saved.customBulletins : [],
    customKudos: Array.isArray(saved.customKudos) ? saved.customKudos : [],
    customPitches: Array.isArray(saved.customPitches) ? saved.customPitches : [],
  };
}

function readState() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (error) {
    return null;
  }
}

function saveState() {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    return;
  }
}

function toggleArrayValue(items, value) {
  return items.includes(value) ? items.filter((item) => item !== value) : [...items, value];
}

function gradientValue(key) {
  return gradients[key] || gradients.warm;
}

function capitalize(value) {
  return value ? value.charAt(0).toUpperCase() + value.slice(1) : "";
}

function initialsFromName(name) {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (!parts.length) {
    return "AC";
  }
  if (parts.length === 1) {
    return parts[0].slice(0, 2).toUpperCase();
  }
  return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
}

function statusLabel(status) {
  const labels = {
    submitted: "Submitted",
    review: "Under review",
    approved: "Approved",
    implemented: "Implemented",
  };
  return labels[status] || capitalize(status);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function showToast(message) {
  if (!elements.toast) {
    return;
  }

  elements.toast.textContent = message;
  elements.toast.classList.add("show");
  window.clearTimeout(toastTimeoutId);
  toastTimeoutId = window.setTimeout(() => {
    elements.toast.classList.remove("show");
  }, 2200);
}

function likeIcon() {
  return `
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017a2 2 0 01-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095a.905.905 0 00-.905.905c0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"></path>
    </svg>
  `;
}

function commentIcon() {
  return `
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
    </svg>
  `;
}

function upvoteIcon() {
  return `
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"></path>
    </svg>
  `;
}
