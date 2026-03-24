const STORAGE_KEY = "acuite-connect-state-v2-live";

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

const DIRECTORY_FILTER_GROUPS = ["company", "location", "department"];
const DIRECTORY_FILTER_GROUP_LABELS = {
  company: "Company",
  location: "Location",
  department: "Department",
};
const COMPANY_DISPLAY_LABELS = {
  Acuite: "Acuité",
};
const COMMUNITY_BOARD_CONFIG = {
  marketplace: {
    label: "Marketplace",
    kicker: "Exchange",
    title: "Give away, barter or sell",
    summary: "Employees can exchange books, gadgets, furniture and useful home items without clutter.",
    metaLabel: "Price or exchange note",
    metaPlaceholder: "Free pickup | Rs 2,000 | Open to barter",
    emptyTitle: "No marketplace posts yet",
    emptyCopy: "The first employee listing for books, gadgets, furniture or other items will appear here.",
    types: [
      { value: "giveaway", label: "Give away" },
      { value: "barter", label: "Barter" },
      { value: "sell", label: "Sell" },
    ],
  },
  housing: {
    label: "Housing",
    kicker: "Stay board",
    title: "Roommate and stay help",
    summary: "A clean internal board for room searches, flatmate requests, paying guest leads and relocation support.",
    metaLabel: "Budget or timing",
    metaPlaceholder: "Budget up to Rs 22,000 | Available from April",
    emptyTitle: "No housing requests yet",
    emptyCopy: "Roommate searches, flat requests and temporary stay leads will appear here.",
    types: [
      { value: "looking_for_roommate", label: "Looking for roommate" },
      { value: "looking_for_place", label: "Looking for a place" },
      { value: "offering_place", label: "Offering a place" },
    ],
  },
  life_moments: {
    label: "Life moments",
    kicker: "Milestones",
    title: "Share important personal news",
    summary: "Marriage, childbirth, a new home or a new car deserve a warmer home than a generic company announcement stream.",
    metaLabel: "When or where",
    metaPlaceholder: "Celebrating this weekend | Ahmedabad | Joined by family",
    emptyTitle: "No life moments have been shared yet",
    emptyCopy: "When someone shares a milestone here, the Community board will carry it with the right amount of warmth.",
    types: [
      { value: "marriage", label: "Marriage" },
      { value: "child_birth", label: "Birth of a child" },
      { value: "new_home", label: "New house" },
      { value: "new_car", label: "New car" },
      { value: "celebration", label: "Other celebration" },
    ],
  },
};
const VOICE_TOPIC_CONFIG = {
  idea: {
    label: "Ideas",
    kicker: "Idea Space",
    title: "Employee ideas worth building on",
    summary: "This is the practical space for better workflows, better tools, better rituals and better ways of working.",
    emptyTitle: "No ideas have been posted yet",
    emptyCopy: "The first live employee idea will appear here and start shaping what Connect should improve next.",
  },
  csr: {
    label: "CSR",
    kicker: "Social Impact",
    title: "CSR proposals and recommendations",
    summary: "Employees can surface causes, partner organisations and thoughtful proposals that deserve formal consideration.",
    emptyTitle: "No CSR proposals have been posted yet",
    emptyCopy: "When someone recommends a CSR initiative or partner, it will appear here for broader employee visibility.",
  },
  ceo_corner: {
    label: "CEO Corner",
    kicker: "Leadership Voice",
    title: "Notes from the MD & CEO",
    summary: "A dedicated lane for high-signal leadership notes, strong opinions, directional commentary and the occasional rant.",
    emptyTitle: "No CEO notes have been posted yet",
    emptyCopy: "CEO corner remains leadership-led. The first published note will appear here.",
  },
};
const VOICE_POLL_OPTION_BACKGROUNDS = [
  "rgba(247,148,29,0.12)",
  "rgba(46,173,43,0.10)",
  "rgba(255,199,44,0.12)",
  "rgba(141,198,63,0.10)",
  "rgba(123,36,28,0.12)",
];

const HOME_PILLARS = [
  {
    kicker: "Community",
    title: "Community Exchange",
    copy: "The practical layer for housing help, internal exchange and life moments.",
    bullets: [
      "Marketplace posts",
      "Roommate and stay notices",
      "Personal milestones",
    ],
    tab: "community",
  },
  {
    kicker: "Voice",
    title: "Ideas & Voice",
    copy: "A clearer home for employee ideas, CEO notes, CSR proposals and quick polls.",
    bullets: [
      "The Pitch",
      "Leadership corner",
      "CSR and pulse checks",
    ],
    tab: "ideas-voice",
  },
  {
    kicker: "Recognition",
    title: "Recognition & Rewards",
    copy: "Appreciation, celebrations and the reward system that will power the brand store.",
    bullets: [
      "The Wall",
      "Birthdays and anniversaries",
      "Points and redemption",
    ],
    tab: "recognition",
  },
];

const HOME_CORE_SPACES = [
  {
    id: "space-community",
    title: "Community Exchange",
    summary: "Buy, sell, barter, give away, ask for housing help and share important life updates.",
    note: "Marketplace, stay board and personal milestones",
    tab: "community",
    initials: "CE",
    gradient: "warm",
    status: "pilot",
  },
  {
    id: "space-learning",
    title: "Clubs & Learning",
    summary: "Book club requisitions, mentoring, training needs and peer-led learning.",
    note: "Book catalog, training requests and mentoring",
    tab: "clubs-learning",
    initials: "CL",
    gradient: "leaf",
    status: "pilot",
  },
  {
    id: "space-ideas",
    title: "Ideas & Voice",
    summary: "A single destination for employee ideas, CEO notes, CSR proposals and polls.",
    note: "Ideas, leadership voice and company pulse",
    tab: "ideas-voice",
    initials: "IV",
    gradient: "fire",
    status: "pilot",
  },
  {
    id: "space-recognition",
    title: "Recognition & Rewards",
    summary: "Public appreciation, celebrations and the future reward points engine.",
    note: "Kudos, milestones and engagement value",
    tab: "recognition",
    initials: "RR",
    gradient: "gold",
    status: "pilot",
  },
  {
    id: "space-store",
    title: "Brand Store",
    summary: "Acuité merchandise and memorabilia, ready for eventual point redemption.",
    note: "Catalog, redemption and inventory rules",
    tab: "store",
    initials: "BS",
    gradient: "ember",
    status: "planned",
  },
  {
    id: "space-business",
    title: "Business Desk",
    summary: "Business updates, client testimonials and leadership communication with durability.",
    note: "Business signals, trust stories and high-signal notes",
    tab: "business",
    initials: "BD",
    gradient: "cool",
    status: "live",
  },
];

const HOME_FOUNDATION_LAYERS = [
  {
    title: "People Directory",
    label: "Find experts by company, city and department",
    note: "This is the people layer behind almost every future workflow.",
    tab: "directory",
  },
  {
    title: "Tool Hub",
    label: "Connect internal apps and workflow surfaces",
    note: "This becomes the operating layer once modules start doing real work.",
    tab: "tools",
  },
  {
    title: "Knowledge Hub",
    label: "Keep policies, templates and decks close to decisions",
    note: "This is the memory layer that supports every business and people workflow.",
    tab: "knowledge",
  },
];

const appData = {
  currentUser: {
    name: "Rahul Mehta",
    initials: "RM",
    role: "Senior Analyst - Ratings",
    city: "Mumbai",
    is_staff: false,
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
  communityPosts: [],
  voicePosts: [],
  activePoll: null,
  learningBooks: [],
  learningRequisitions: [],
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

Object.assign(appData, {
  agenda: [],
  tasks: [],
  pulse: [],
  communityPosts: [],
  voicePosts: [],
  activePoll: null,
  learningBooks: [],
  learningRequisitions: [],
  homePosts: [],
  bulletinPosts: [],
  wallPosts: [],
  leaderboard: [],
  clubs: [],
  spotlights: [],
  pitches: [],
  moments: [],
  alumni: [],
  directory: [],
  knowledgeItems: [],
  birthdays: [],
  anniversaries: [],
  upcoming: [],
  pollOptions: [],
});

let directoryFilterOptions = createDirectoryFilterOptions();

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
  communityFilter: "all",
  voiceFilter: "all",
  learningBookFilter: "all",
  learningBookQuery: "",
  bulletinFilter: "all",
  pitchFilter: "trending",
  momentsFilter: "all",
  knowledgeFilter: "all",
  directoryFilters: createDirectoryFiltersState(),
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
let directoryLoadError = "";
let communityLoadError = "";
let voiceLoadError = "";
let learningLoadError = "";

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
      role: authenticatedUser.title || appData.currentUser.role,
      city: authenticatedUser.location || appData.currentUser.city,
      is_staff: Boolean(authenticatedUser.is_staff),
    };
  }

  elements = {
    searchInput: document.getElementById("global-search"),
    searchResults: document.getElementById("search-results"),
    directorySearchInput: document.getElementById("directory-search"),
    learningBookSearchInput: document.getElementById("learning-book-search"),
    communityForm: document.getElementById("community-form"),
    communityBoardSelect: document.getElementById("community-board-select"),
    communityTypeSelect: document.getElementById("community-type-select"),
    communityMetaLabel: document.getElementById("community-meta-label"),
    communityMetaInput: document.getElementById("community-meta-input"),
    voiceForm: document.getElementById("voice-form"),
    voiceTopicSelect: document.getElementById("voice-topic-select"),
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

  await Promise.all([loadDirectoryData(), loadCommunityPosts(), loadVoiceData(), loadLearningData()]);
  bindEvents();
  renderAll();
}

async function loadDirectoryData() {
  directoryLoadError = "";
  directoryFilterOptions = createDirectoryFilterOptions();
  appData.directory = [];

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    directoryLoadError = "Directory services are unavailable in this build.";
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/directory/");
    appData.directory = Array.isArray(payload.results)
      ? payload.results.map(mapDirectoryProfileToCard)
      : [];
    directoryFilterOptions = {
      company: Array.isArray(payload.filters?.company) ? payload.filters.company : [],
      location: Array.isArray(payload.filters?.location) ? payload.filters.location : [],
      department: Array.isArray(payload.filters?.department) ? payload.filters.department : [],
    };
  } catch (error) {
    directoryLoadError = error.message || "Could not load the people directory.";
  }
}

async function loadCommunityPosts() {
  communityLoadError = "";
  appData.communityPosts = [];

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    communityLoadError = "Community services are unavailable in this build.";
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/?module=community");
    appData.communityPosts = Array.isArray(payload.results)
      ? payload.results.map(mapCommunityPost)
      : [];
  } catch (error) {
    communityLoadError = error.message || "Could not load community posts.";
  }
}

async function loadLearningData() {
  learningLoadError = "";
  appData.learningBooks = [];
  appData.learningRequisitions = [];

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    learningLoadError = "Learning services are unavailable in this build.";
    return;
  }

  try {
    const [booksPayload, requisitionsPayload] = await Promise.all([
      window.AcuiteConnectAuth.apiRequest("/api/learning/books/"),
      window.AcuiteConnectAuth.apiRequest("/api/learning/requisitions/"),
    ]);
    appData.learningBooks = Array.isArray(booksPayload.results) ? booksPayload.results : [];
    appData.learningRequisitions = Array.isArray(requisitionsPayload.results) ? requisitionsPayload.results : [];
  } catch (error) {
    learningLoadError = error.message || "Could not load book-club data.";
  }
}

async function loadVoiceData() {
  voiceLoadError = "";
  appData.voicePosts = [];
  appData.activePoll = null;

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    voiceLoadError = "Ideas & Voice services are unavailable in this build.";
    return;
  }

  try {
    const [postsPayload, pollPayload] = await Promise.all([
      window.AcuiteConnectAuth.apiRequest("/api/feed/posts/?module=ideas_voice"),
      window.AcuiteConnectAuth.apiRequest("/api/voice/polls/active/"),
    ]);
    appData.voicePosts = Array.isArray(postsPayload.results)
      ? postsPayload.results.map(mapVoicePost)
      : [];
    appData.activePoll = pollPayload.poll ? mapVoicePoll(pollPayload.poll) : null;
  } catch (error) {
    voiceLoadError = error.message || "Could not load Ideas & Voice.";
  }
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

  if (elements.communityBoardSelect) {
    elements.communityBoardSelect.addEventListener("change", () => {
      syncCommunityComposer();
    });
  }

  if (elements.voiceTopicSelect) {
    elements.voiceTopicSelect.addEventListener("change", () => {
      syncVoiceComposer();
    });
  }

  if (elements.learningBookSearchInput) {
    elements.learningBookSearchInput.addEventListener("input", (event) => {
      state.learningBookQuery = event.target.value;
      saveState();
      renderLearningPanel();
    });
  }

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
      await voteOnPoll(action.dataset.id);
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

    if (actionName === "request-book") {
      await requestBook(action.dataset.id);
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

  const directoryChip = event.target.closest("[data-directory-filter-group]");
  if (directoryChip) {
    const group = directoryChip.dataset.directoryFilterGroup;
    const value = directoryChip.dataset.directoryFilterValue;
    state.directoryFilters[group] = toggleDirectoryFilterSelection(state.directoryFilters[group], value);
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
  if (event.target === elements.communityForm) {
    event.preventDefault();
    void submitCommunity();
    return;
  }

  if (event.target === elements.voiceForm) {
    event.preventDefault();
    void submitVoicePost();
    return;
  }

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
  renderCommunityPanel();
  renderVoicePanel();
  renderLearningPanel();
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
  const receivedKudos = state.customKudos.filter((item) => item.recipient.toLowerCase() === appData.currentUser.name.toLowerCase()).length;
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
      label: "Core spaces",
      value: "6",
      note: "Community, learning, voice, rewards, store and business",
    },
    {
      label: "Foundation layers",
      value: "3",
      note: "Directory, tools and knowledge support every module",
    },
    {
      label: "Vision items",
      value: "14",
      note: "The current feature list now has clear homes inside Connect",
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
  renderHomePillar("today-panel", HOME_PILLARS[0]);
}

function renderTasksPanel() {
  renderHomePillar("tasks-panel", HOME_PILLARS[1]);
}

function renderPulsePanel() {
  renderHomePillar("pulse-panel", HOME_PILLARS[2]);
}

function renderHomeTools() {
  document.getElementById("home-tools-grid").innerHTML = HOME_CORE_SPACES.map(renderHomeSpaceCard).join("");
}

function renderHomeFeed() {
  document.getElementById("home-feed").innerHTML = HOME_FOUNDATION_LAYERS.map((layer) => `
    <article class="summary-card foundation-card">
      <strong>${escapeHtml(layer.title)}</strong>
      <span>${escapeHtml(layer.label)}</span>
      <p>${escapeHtml(layer.note)}</p>
      <button type="button" class="btn-link" data-switch-tab="${layer.tab}">Open</button>
    </article>
  `).join("");
}

function renderCommunityPanel() {
  syncCommunityComposer();
  renderCommunitySummary();
  renderCommunityGuideCards();
  renderCommunityFeed();
}

function renderLearningPanel() {
  renderLearningSummary();
  renderLearningBooks();
  renderLearningRequisitions();
  renderLearningGuideCards();
}

function renderVoicePanel() {
  syncVoiceComposer();
  renderVoiceSummary();
  renderVoiceFeed();
  renderVoicePollCard();
  renderVoiceGuidanceCard();
}

function renderCommunitySummary() {
  const posts = getFilteredCommunityPosts();
  const allPosts = appData.communityPosts;
  const activeCities = new Set(
    allPosts.map((post) => post.city).filter(Boolean).map((city) => city.toLowerCase()),
  ).size;
  const latestPost = allPosts[0];
  const boardLabel = state.communityFilter === "all"
    ? "All boards"
    : getCommunityBoardLabel(state.communityFilter);

  document.getElementById("community-summary-grid").innerHTML = [
    {
      kicker: "Live now",
      title: `${allPosts.length} shared posts`,
      copy: "Real employee posts published inside Community Exchange.",
    },
    {
      kicker: "Coverage",
      title: `${activeCities} active cities`,
      copy: activeCities ? "City tags make it easier to scan the right local board." : "City-based activity will begin to show once posts start coming in.",
    },
    {
      kicker: "Board filter",
      title: boardLabel,
      copy: latestPost
        ? `Latest post: ${latestPost.title}`
        : "No posts yet. The first live listing will set the pace for this module.",
    },
  ].map((item) => `
    <article class="mini-panel">
      <p class="widget-kicker">${escapeHtml(item.kicker)}</p>
      <h3>${escapeHtml(item.title)}</h3>
      <p class="muted-copy">${escapeHtml(item.copy)}</p>
    </article>
  `).join("");

  document.getElementById("community-results-meta").textContent = allPosts.length
    ? `${posts.length} of ${allPosts.length} live community posts shown`
    : "Live employee community board";
}

function renderCommunityGuideCards() {
  const activeBoard = state.communityFilter === "all" ? "marketplace" : state.communityFilter;
  const board = COMMUNITY_BOARD_CONFIG[activeBoard] || COMMUNITY_BOARD_CONFIG.marketplace;
  const hotCities = summarizeCommunityCities();

  document.getElementById("community-guide-card").innerHTML = `
    <p class="widget-kicker">${escapeHtml(board.kicker)}</p>
    <h3>${escapeHtml(board.title)}</h3>
    <p>${escapeHtml(board.summary)}</p>
    <ul class="simple-list">
      ${board.types.map((type) => `<li>${escapeHtml(type.label)}</li>`).join("")}
    </ul>
  `;

  document.getElementById("community-city-card").innerHTML = `
    <p class="widget-kicker">City pulse</p>
    <h3>Where community activity is surfacing</h3>
    ${
      hotCities.length
        ? `<ul class="mini-list community-city-list">
            ${hotCities.map((item) => `
              <li>
                <div>
                  <div class="mini-item-title">${escapeHtml(item.city)}</div>
                  <div class="mini-item-meta">${escapeHtml(item.note)}</div>
                </div>
                <div class="mini-item-time">${escapeHtml(String(item.count))}</div>
              </li>
            `).join("")}
          </ul>`
        : `<div class="empty-state">Once employees begin posting, the most active cities will surface here automatically.</div>`
    }
  `;
}

function renderCommunityFeed() {
  const container = document.getElementById("community-feed");
  if (communityLoadError) {
    container.innerHTML = `<div class="empty-state">${escapeHtml(communityLoadError)}</div>`;
    return;
  }

  const posts = getFilteredCommunityPosts();
  if (!appData.communityPosts.length) {
    container.innerHTML = `
      <div class="empty-state">
        No live Community Exchange posts have been shared yet. The first employee listing or announcement will appear here.
      </div>
    `;
    return;
  }

  if (!posts.length) {
    const board = COMMUNITY_BOARD_CONFIG[state.communityFilter];
    container.innerHTML = `
      <div class="empty-state">
        ${escapeHtml(board ? board.emptyCopy : "No posts match the selected board right now.")}
      </div>
    `;
    return;
  }

  container.innerHTML = posts.map(renderCommunityPostCard).join("");
}

function renderLearningSummary() {
  const filteredBooks = getFilteredLearningBooks();
  const availableTitles = appData.learningBooks.filter((book) => book.available_copies > 0).length;
  const myOpenRequests = appData.learningRequisitions.filter((item) => isOpenLearningStatus(item.status)).length;

  document.getElementById("learning-summary-grid").innerHTML = [
    {
      kicker: "Book Club",
      title: `${appData.learningBooks.length} titles`,
      copy: "Admin-managed library titles ready for employee requisitions.",
    },
    {
      kicker: "Availability",
      title: `${availableTitles} ready now`,
      copy: "Titles with at least one copy still open for requisition.",
    },
    {
      kicker: "Your queue",
      title: `${myOpenRequests} open request${myOpenRequests === 1 ? "" : "s"}`,
      copy: filteredBooks.length
        ? `${filteredBooks.length} titles match your current filter.`
        : "Search and filter the catalog to find the right title faster.",
    },
  ].map((item) => `
    <article class="mini-panel">
      <p class="widget-kicker">${escapeHtml(item.kicker)}</p>
      <h3>${escapeHtml(item.title)}</h3>
      <p class="muted-copy">${escapeHtml(item.copy)}</p>
    </article>
  `).join("");
}

function renderLearningBooks() {
  const container = document.getElementById("learning-book-grid");
  if (elements.learningBookSearchInput) {
    elements.learningBookSearchInput.value = state.learningBookQuery;
  }

  if (learningLoadError) {
    document.getElementById("learning-results-meta").textContent = "Learning services issue";
    container.innerHTML = `<div class="empty-state">${escapeHtml(learningLoadError)}</div>`;
    return;
  }

  const books = getFilteredLearningBooks();
  document.getElementById("learning-results-meta").textContent = appData.learningBooks.length
    ? `${books.length} of ${appData.learningBooks.length} titles shown`
    : "Live Acuité book club catalog";

  if (!appData.learningBooks.length) {
    container.innerHTML = `
      <div class="empty-state">
        The book catalog is empty right now. Once admins upload titles in the backend, employees will be able to requisition them here.
      </div>
    `;
    return;
  }

  if (!books.length) {
    container.innerHTML = `
      <div class="empty-state">
        No titles match that search or filter. Try a broader title, author or availability view.
      </div>
    `;
    return;
  }

  container.innerHTML = books.map(renderLearningBookCard).join("");
}

function renderLearningRequisitions() {
  const openItems = appData.learningRequisitions.filter((item) => isOpenLearningStatus(item.status));
  const closedItems = appData.learningRequisitions.filter((item) => !isOpenLearningStatus(item.status));
  const items = [...openItems, ...closedItems].slice(0, 6);

  document.getElementById("learning-my-requisitions").innerHTML = `
    <p class="widget-kicker">My requisitions</p>
    <h3>Your reading queue</h3>
    ${
      items.length
        ? `<ul class="mini-list learning-req-list">
            ${items.map((item) => `
              <li>
                <div>
                  <div class="mini-item-title">${escapeHtml(item.book.title)}</div>
                  <div class="mini-item-meta">${escapeHtml(item.book.author)}</div>
                </div>
                <div class="learning-req-status ${escapeHtml(item.status)}">${escapeHtml(learningStatusLabel(item.status))}</div>
              </li>
            `).join("")}
          </ul>`
        : `<div class="empty-state">You have not requisitioned any books yet.</div>`
    }
  `;
}

function renderLearningGuideCards() {
  document.getElementById("learning-guidance-card").innerHTML = `
    <p class="widget-kicker">How it works</p>
    <h3>Book requisitions made simple</h3>
    <ul class="simple-list">
      <li>Admins upload titles and authors into the catalog.</li>
      <li>Employees request a title with one click.</li>
      <li>Approvals, issue and return tracking stay visible in admin.</li>
    </ul>
  `;

  document.getElementById("learning-next-card").innerHTML = `
    <p class="widget-kicker">Coming next</p>
    <h3>Mentoring and training exchange</h3>
    <p>After the book workflow, this module is ready for skill requests, internal mentors and peer-led sessions.</p>
  `;
}

function renderVoiceSummary() {
  const filteredPosts = getFilteredVoicePosts();
  const ideaCount = appData.voicePosts.filter((post) => post.topic === "idea").length;
  const ceoCount = appData.voicePosts.filter((post) => post.topic === "ceo_corner").length;
  const csrCount = appData.voicePosts.filter((post) => post.topic === "csr").length;

  document.getElementById("voice-summary-grid").innerHTML = [
    {
      kicker: "Ideas",
      title: `${ideaCount} live`,
      copy: "Employee suggestions that can shape operations, culture, product and workflow design.",
    },
    {
      kicker: "CEO corner",
      title: `${ceoCount} note${ceoCount === 1 ? "" : "s"}`,
      copy: "Leadership-led commentary that deserves a durable lane inside Connect.",
    },
    {
      kicker: "CSR",
      title: `${csrCount} proposal${csrCount === 1 ? "" : "s"}`,
      copy: "Social-impact recommendations that can mature into formal company initiatives.",
    },
    {
      kicker: "Quick poll",
      title: appData.activePoll ? `${appData.activePoll.total_votes} vote${appData.activePoll.total_votes === 1 ? "" : "s"}` : "No active poll",
      copy: appData.activePoll
        ? appData.activePoll.question
        : "Admins can publish a live pulse question from the backend when needed.",
    },
  ].map((item) => `
    <article class="mini-panel">
      <p class="widget-kicker">${escapeHtml(item.kicker)}</p>
      <h3>${escapeHtml(item.title)}</h3>
      <p class="muted-copy">${escapeHtml(item.copy)}</p>
    </article>
  `).join("");

  document.getElementById("voice-results-meta").textContent = appData.voicePosts.length
    ? `${filteredPosts.length} of ${appData.voicePosts.length} live voice posts shown`
    : "Live employee ideas, leadership notes and CSR proposals";
}

function renderVoiceFeed() {
  const container = document.getElementById("voice-feed");
  if (voiceLoadError) {
    container.innerHTML = `<div class="empty-state">${escapeHtml(voiceLoadError)}</div>`;
    return;
  }

  const posts = getFilteredVoicePosts();
  if (!appData.voicePosts.length) {
    container.innerHTML = `
      <div class="empty-state">
        No live Ideas &amp; Voice posts have been shared yet. This space is ready for ideas, CSR recommendations and leadership notes.
      </div>
    `;
    return;
  }

  if (!posts.length) {
    const topic = VOICE_TOPIC_CONFIG[state.voiceFilter];
    container.innerHTML = `
      <div class="empty-state">
        ${escapeHtml(topic ? topic.emptyCopy : "No posts match this filter right now.")}
      </div>
    `;
    return;
  }

  container.innerHTML = posts.map(renderVoicePostCard).join("");
}

function renderVoicePollCard() {
  const container = document.getElementById("voice-poll-card");
  if (!container) {
    return;
  }

  if (voiceLoadError && !appData.activePoll) {
    container.innerHTML = `
      <p class="widget-kicker">Quick poll</p>
      <h3>Live poll unavailable</h3>
      <div class="empty-state">${escapeHtml(voiceLoadError)}</div>
    `;
    return;
  }

  if (!appData.activePoll) {
    container.innerHTML = `
      <p class="widget-kicker">Quick poll</p>
      <h3>No active poll right now</h3>
      <div class="empty-state">When leadership publishes a pulse question, employees will be able to vote here live.</div>
    `;
    return;
  }

  container.innerHTML = `
    <p class="widget-kicker">Quick poll</p>
    <h3>${escapeHtml(appData.activePoll.question)}</h3>
    ${appData.activePoll.description ? `<p class="poll-question">${escapeHtml(appData.activePoll.description)}</p>` : ""}
    <div class="poll-stack">
      ${renderPollOptions(appData.activePoll)}
    </div>
    <div class="widget-footnote">
      ${appData.activePoll.is_open ? "Votes update live for the active poll." : "This poll is closed. Results stay visible for reference."}
    </div>
  `;
}

function renderVoiceGuidanceCard() {
  const container = document.getElementById("voice-guidance-card");
  if (!container) {
    return;
  }

  const activeTopic = state.voiceFilter === "all" ? null : VOICE_TOPIC_CONFIG[state.voiceFilter];
  const topicSummary = activeTopic
    ? activeTopic.summary
    : "Ideas & Voice combines employee ideas, CSR proposals, leadership notes and live pulse checks in one clearer destination.";

  container.innerHTML = `
    <p class="widget-kicker">${escapeHtml(activeTopic ? activeTopic.kicker : "Posting guide")}</p>
    <h3>${escapeHtml(activeTopic ? activeTopic.title : "How this space is split")}</h3>
    <p>${escapeHtml(topicSummary)}</p>
    <ul class="simple-list">
      <li>Ideas are for workflow, product, process and culture improvements.</li>
      <li>CSR is for thoughtful causes, partnerships and impact proposals.</li>
      <li>CEO corner stays leadership-led and appears only to staff in the composer.</li>
    </ul>
  `;
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
  document.getElementById("wall-feed").innerHTML = posts.length
    ? posts.map(renderKudosPost).join("")
    : `<div class="empty-state">Recognition posts will appear here once employees start sharing kudos.</div>`;
}

function renderLeaderboard() {
  if (!appData.leaderboard.length) {
    document.getElementById("leaderboard-card").innerHTML = `
      <p class="widget-kicker">Recognition</p>
      <h3>Most appreciated this month</h3>
      <div class="empty-state">Recognition rankings will appear after live usage begins.</div>
    `;
    return;
  }
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
  document.getElementById("clubs-grid").innerHTML = appData.clubs.length ? appData.clubs.map((club) => {
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
  }).join("") : `<div class="empty-state">Clubs will appear here when the first live communities are created.</div>`;
}

function renderSpotlight() {
  if (!appData.spotlights.length) {
    document.getElementById("spotlight-feature").innerHTML = `<div class="empty-state">No live spotlight stories have been published yet.</div>`;
    document.getElementById("previous-spotlights").innerHTML = "";
    return;
  }
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
  document.getElementById("moments-grid").innerHTML = items.length ? items.map((moment) => `
    <article class="moment-item" id="${moment.id}" style="background:${moment.background}">
      <div class="moment-placeholder">${moment.emoji}</div>
      <div class="overlay">
        <p>${escapeHtml(moment.title)}</p>
        <span>${escapeHtml(String(moment.photos))} photos</span>
      </div>
    </article>
  `).join("") : `<div class="empty-state">No live moments have been shared yet.</div>`;
}

function renderAlumni() {
  document.getElementById("alumni-grid").innerHTML = appData.alumni.length ? appData.alumni.map((person) => `
    <article class="alumni-card" id="${person.id}">
      <div class="alumni-avatar" style="background:${gradientValue(person.gradient)}">${escapeHtml(person.initials)}</div>
      <h4>${escapeHtml(person.name)}</h4>
      <div class="alumni-current">${escapeHtml(person.current)}</div>
      <div class="alumni-badge">${escapeHtml(person.batch)}</div>
      <div class="alumni-tenure">${escapeHtml(person.tenure)}</div>
      <button type="button" class="connect-btn" data-action="connect-alumni" data-name="${escapeHtml(person.name)}">Connect</button>
    </article>
  `).join("") : `<div class="empty-state">Alumni records will appear when that directory is activated.</div>`;
}

function renderDirectoryChips() {
  document.getElementById("directory-filter-groups").innerHTML = DIRECTORY_FILTER_GROUPS.map((groupId) => {
    const options = directoryFilterOptions[groupId] || [];
    const selectedValues = state.directoryFilters[groupId] || [];
    const buttons = [{ value: "all", label: "All" }, ...options.map((value) => ({
      value,
      label: displayDirectoryFilterLabel(groupId, value),
    }))];
    return `
      <div class="directory-filter-group">
        <div class="directory-filter-title">${escapeHtml(DIRECTORY_FILTER_GROUP_LABELS[groupId])}</div>
        <div class="directory-filter-buttons">
          ${buttons.map((option) => `
            <button
              type="button"
              class="${isDirectoryFilterOptionActive(selectedValues, option.value) ? "active" : ""}"
              data-directory-filter-group="${groupId}"
              data-directory-filter-value="${escapeHtml(option.value)}"
            >
              ${escapeHtml(option.label)}
            </button>
          `).join("")}
        </div>
      </div>
    `;
  }).join("");
}

function renderDirectory() {
  elements.directorySearchInput.value = state.directoryQuery;
  const query = state.directoryQuery.trim().toLowerCase();
  const selectedCompanies = state.directoryFilters.company || [];
  const selectedLocations = state.directoryFilters.location || [];
  const selectedDepartments = state.directoryFilters.department || [];
  const filtered = appData.directory.filter((person) => {
    if (selectedCompanies.length && !selectedCompanies.includes(person.company)) {
      return false;
    }
    if (selectedLocations.length && !selectedLocations.includes(person.office)) {
      return false;
    }
    if (selectedDepartments.length && !selectedDepartments.includes(person.department)) {
      return false;
    }
    if (!query) {
      return true;
    }
    return person.searchText.includes(query);
  });

  if (directoryLoadError) {
    document.getElementById("directory-results-meta").textContent = "Directory load issue";
    document.getElementById("directory-grid").innerHTML = `<div class="empty-state">${escapeHtml(directoryLoadError)}</div>`;
    return;
  }

  document.getElementById("directory-results-meta").textContent = appData.directory.length
    ? `${filtered.length} of ${appData.directory.length} employees shown`
    : "Live employee directory";

  if (!appData.directory.length) {
    document.getElementById("directory-grid").innerHTML = `<div class="empty-state">The people directory will appear here once the live employee import completes.</div>`;
    return;
  }

  document.getElementById("directory-grid").innerHTML = filtered.length
    ? filtered.map((person) => `
      <article class="person-card" id="${person.id}">
        <div class="person-head">
          <div class="person-avatar" style="background:${gradientValue(person.gradient)}">${escapeHtml(person.initials)}</div>
          <div class="person-meta">
            <h3>${escapeHtml(person.name)}</h3>
            <div class="person-role">${escapeHtml(person.role)}</div>
            <div class="person-location">${escapeHtml(person.officeLine)}</div>
          </div>
        </div>
        <div class="person-detail-grid">
          ${directoryCardDetail("Employee Code", person.employeeCode)}
          ${directoryCardDetail("Company", person.companyLabel || person.company)}
          ${directoryCardDetail("Department", person.department)}
          ${directoryCardDetail("Function", person.functionName)}
          ${directoryCardDetail("Office", person.office)}
          ${directoryCardDetail("Joined", person.joinedOn)}
        </div>
        <div class="team-row">
          ${person.teams.map((team) => `<span class="team-chip">${escapeHtml(team)}</span>`).join("")}
        </div>
        <div class="person-footer">
          <span class="availability">${escapeHtml(person.contactLine)}</span>
          <button type="button" class="btn-outline" data-action="show-person" data-name="${escapeHtml(person.name)}">View details</button>
        </div>
      </article>
    `).join("")
    : `<div class="empty-state">No people matched that filter. Try a broader company, location, or department selection.</div>`;
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
  document.getElementById("birthdays-list").innerHTML = appData.birthdays.length ? appData.birthdays.map((person) => `
    <div class="bday-item">
      <div class="bday-avatar" style="background:${gradientValue(person.gradient)}">${escapeHtml(person.initials)}</div>
      <div class="bday-info">
        <div class="name">${escapeHtml(person.name)}</div>
        <div class="date ${person.highlight ? "today" : ""}">${escapeHtml(person.date)}</div>
      </div>
    </div>
  `).join("") : `<div class="empty-state">Birthday highlights will appear once live employee celebrations are configured.</div>`;
}

function renderAnniversaries() {
  document.getElementById("anniversaries-list").innerHTML = appData.anniversaries.length ? appData.anniversaries.map((person) => `
    <div class="bday-item">
      <div class="bday-avatar" style="background:${gradientValue(person.gradient)}">${escapeHtml(person.initials)}</div>
      <div class="bday-info">
        <div class="name">${escapeHtml(person.name)}</div>
        <div class="date ${person.highlight ? "today" : ""}">${escapeHtml(person.date)}</div>
      </div>
    </div>
  `).join("") : `<div class="empty-state">Work anniversary highlights will appear here later.</div>`;
}

function renderUpcoming() {
  document.getElementById("upcoming-events").innerHTML = appData.upcoming.length ? appData.upcoming.map((item) => `
    <div class="event-item">
      <div class="event-date">${escapeHtml(item.date)}</div>
      <div class="event-name">${escapeHtml(item.name)}</div>
    </div>
  `).join("") : `<div class="empty-state">No live internal events have been published yet.</div>`;
}

function renderPoll() {
  const questionElement = document.getElementById("poll-question");
  const listElement = document.getElementById("poll-list");
  if (!listElement) {
    return;
  }

  if (!appData.activePoll) {
    if (questionElement) {
      questionElement.textContent = "No live poll is running right now.";
    }
    listElement.innerHTML = `<div class="empty-state">The next company pulse question will appear here when it is published.</div>`;
    return;
  }

  if (questionElement) {
    questionElement.textContent = appData.activePoll.question;
  }
  listElement.innerHTML = renderPollOptions(appData.activePoll);
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

function renderHomeSpaceCard(space) {
  return `
    <article class="tool-card module-card" id="${space.id}">
      <div class="tool-card-head">
        <div class="tool-icon" style="background:${gradientValue(space.gradient)}">${escapeHtml(space.initials)}</div>
        <div>
          <h3>${escapeHtml(space.title)}</h3>
          <span class="tool-status ${space.status}">${escapeHtml(capitalize(space.status))}</span>
        </div>
      </div>
      <p>${escapeHtml(space.summary)}</p>
      <div class="tool-meta">
        <span class="mini-item-meta">${escapeHtml(space.note)}</span>
        <button type="button" class="tool-open" data-switch-tab="${space.tab}">Explore</button>
      </div>
    </article>
  `;
}

function renderHomePillar(elementId, pillar) {
  const element = document.getElementById(elementId);
  if (!element) {
    return;
  }
  element.innerHTML = `
    <p class="widget-kicker">${escapeHtml(pillar.kicker)}</p>
    <h3>${escapeHtml(pillar.title)}</h3>
    <p class="muted-copy">${escapeHtml(pillar.copy)}</p>
    <ul class="simple-list">
      ${pillar.bullets.map((bullet) => `<li>${escapeHtml(bullet)}</li>`).join("")}
    </ul>
    <button type="button" class="btn-link" data-switch-tab="${pillar.tab}">Open space</button>
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

function renderCommunityPostCard(post) {
  return `
    <article class="card community-card community-board-${escapeHtml(post.board)}" id="${post.id}">
      <div class="community-card-top">
        <div class="community-card-tags">
          <span class="mini-chip">${escapeHtml(post.boardLabel)}</span>
          <span class="mini-chip success">${escapeHtml(post.typeLabel)}</span>
          ${post.city ? `<span class="mini-chip">${escapeHtml(post.city)}</span>` : ""}
        </div>
        <div class="community-time">${escapeHtml(post.postedAtLabel)}</div>
      </div>
      <div class="card-header">
        <div class="card-avatar" style="background:${gradientValue(post.avatar)}">${escapeHtml(post.initials)}</div>
        <div class="card-meta">
          <div class="card-name">${escapeHtml(post.authorName)}</div>
          <div class="card-sub">${escapeHtml(post.authorMeta)}</div>
        </div>
      </div>
      <div class="card-body">
        <div class="card-title">${escapeHtml(post.title)}</div>
        <p>${escapeHtml(post.body)}</p>
      </div>
      ${
        post.metaLine
          ? `<div class="community-detail-row">
              <span class="community-detail-label">${escapeHtml(post.metaLabel)}</span>
              <strong>${escapeHtml(post.metaLine)}</strong>
            </div>`
          : ""
      }
      <div class="card-actions">
        <button type="button" class="action-btn" data-action="placeholder-comment">
          ${commentIcon()}${escapeHtml(String(post.commentCount))}
        </button>
        <div class="spacer"></div>
        <button
          type="button"
          class="btn-outline"
          data-action="post-cta"
          data-message="${escapeHtml(`Reach out to ${post.authorName} directly for this ${post.boardLabel.toLowerCase()} post.`)}"
        >
          Connect
        </button>
      </div>
    </article>
  `;
}

function renderLearningBookCard(book) {
  const statusText = book.available_copies > 0
    ? `${book.available_copies} of ${book.total_copies} available`
    : "Fully requisitioned";
  const requestLabel = book.requester_has_open_requisition
    ? "Already requested"
    : book.available_copies > 0
      ? "Request book"
      : "Unavailable";

  return `
    <article class="tool-card learning-book-card" id="book-${book.id}">
      <div class="tool-card-head">
        <div class="tool-icon" style="background:${gradientValue(gradientKeyFromText(`${book.title}-${book.author}`))}">
          ${escapeHtml(initialsFromName(book.author))}
        </div>
        <div>
          <h3>${escapeHtml(book.title)}</h3>
          <span class="tool-status ${book.available_copies > 0 ? "live" : "planned"}">${escapeHtml(statusText)}</span>
        </div>
      </div>
      <p class="learning-book-author">${escapeHtml(book.author)}</p>
      <p>${escapeHtml(book.summary || "Ready for requisition by employees through the internal book club.")}</p>
      <div class="tool-meta learning-book-meta">
        <span class="mini-item-meta">${escapeHtml(`${book.open_requisition_count} active requisition${book.open_requisition_count === 1 ? "" : "s"}`)}</span>
        <button
          type="button"
          class="tool-open ${book.can_request ? "live" : ""}"
          data-action="request-book"
          data-id="${book.id}"
          ${book.can_request ? "" : "disabled"}
        >
          ${escapeHtml(requestLabel)}
        </button>
      </div>
    </article>
  `;
}

async function submitCommunity() {
  const formData = new FormData(elements.communityForm);
  const board = String(formData.get("board") || "marketplace");
  const communityType = String(formData.get("community_type") || "").trim();
  const city = String(formData.get("city") || "").trim();
  const metaLine = String(formData.get("meta_line") || "").trim();
  const title = String(formData.get("title") || "").trim();
  const details = String(formData.get("details") || "").trim();

  if (!title || !details || !city || !communityType) {
    showToast("Add board, type, city, title and details before posting.");
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
      method: "POST",
      body: {
        title,
        body: details,
        module: "community",
        topic: board,
        metadata: {
          community_type: communityType,
          city,
          meta_line: metaLine,
        },
      },
    });

    if (payload.post) {
      appData.communityPosts.unshift(mapCommunityPost(payload.post));
      elements.communityForm.reset();
      if (elements.communityBoardSelect) {
        elements.communityBoardSelect.value = board;
      }
      syncCommunityComposer();
      renderCommunityPanel();
      showToast("Community post shared live inside Connect.");
      return;
    }

    showToast("Community post created.");
  } catch (error) {
    showToast(error.message || "Could not share the community post.");
  }
}

async function requestBook(bookId) {
  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/learning/requisitions/", {
      method: "POST",
      body: {
        book_id: Number(bookId),
      },
    });

    if (payload.requisition) {
      await loadLearningData();
      renderLearningPanel();
      showToast(`Book requisition placed for ${payload.requisition.book.title}.`);
      return;
    }

    showToast("Book requisition submitted.");
  } catch (error) {
    showToast(error.message || "Could not place the book requisition.");
  }
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
  const community = appData.communityPosts.map((post) => ({
    title: post.title,
    subtitle: `${post.boardLabel} - ${post.city || "Community Exchange"}`,
    type: "community",
    tab: "community",
    targetId: post.id,
    searchText: [
      post.title,
      post.body,
      post.boardLabel,
      post.typeLabel,
      post.city,
      post.authorName,
      post.metaLine,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase(),
  }));

  const voice = appData.voicePosts.map((post) => ({
    title: post.title,
    subtitle: `${post.topicLabel} - ${post.authorName}`,
    type: "voice",
    tab: "ideas-voice",
    targetId: post.id,
    searchText: [
      post.title,
      post.body,
      post.topicLabel,
      post.authorName,
      post.authorMeta,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase(),
  }));

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

  const books = appData.learningBooks.map((book) => ({
    title: book.title,
    subtitle: `${book.author} - Book Club`,
    type: "book",
    tab: "clubs-learning",
    targetId: `book-${book.id}`,
    searchText: [book.title, book.author, book.summary].filter(Boolean).join(" ").toLowerCase(),
  }));
  const poll = appData.activePoll
    ? [{
      title: appData.activePoll.question,
      subtitle: "Quick Poll - Ideas & Voice",
      type: "poll",
      tab: "ideas-voice",
      targetId: "voice-poll-card",
      searchText: [
        appData.activePoll.question,
        appData.activePoll.description,
        ...appData.activePoll.options.map((option) => option.label),
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase(),
    }]
    : [];

  return [...community, ...voice, ...bulletin, ...directory, ...tools, ...resources, ...books, ...poll];
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
  if (group === "community") {
    state.communityFilter = value;
    saveState();
    renderCommunityPanel();
    syncFilterButtons();
    return;
  }

  if (group === "voice") {
    state.voiceFilter = value;
    saveState();
    renderVoicePanel();
    syncFilterButtons();
    return;
  }

  if (group === "learning-books") {
    state.learningBookFilter = value;
    saveState();
    renderLearningPanel();
    syncFilterButtons();
    return;
  }

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
    community: state.communityFilter,
    voice: state.voiceFilter,
    "learning-books": state.learningBookFilter,
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

function mapCommunityPost(post) {
  const metadata = post.metadata || {};
  const board = post.topic || "marketplace";
  const boardConfig = COMMUNITY_BOARD_CONFIG[board] || COMMUNITY_BOARD_CONFIG.marketplace;
  const communityType = metadata.community_type || boardConfig.types[0].value;
  const typeLabel = getCommunityTypeLabel(board, communityType);
  const author = post.author || {};

  return {
    id: `community-post-${post.id}`,
    sourceId: post.id,
    title: post.title,
    body: post.body,
    board,
    boardLabel: boardConfig.label,
    type: communityType,
    typeLabel,
    city: metadata.city || "",
    metaLine: metadata.meta_line || "",
    metaLabel: boardConfig.metaLabel,
    commentCount: post.comment_count || 0,
    authorName: author.name || "Acuité employee",
    authorMeta: [author.title, author.location].filter(Boolean).join(" | ") || author.email || "Employee",
    initials: author.initials || initialsFromName(author.name || "Acuité"),
    avatar: gradientKeyFromText(`${author.name || ""}-${board}-${communityType}`),
    postedAtLabel: formatRelativeTime(post.published_at || post.created_at),
    createdAt: post.created_at || "",
  };
}

function mapVoicePost(post) {
  const topic = post.topic || "idea";
  const topicConfig = VOICE_TOPIC_CONFIG[topic] || VOICE_TOPIC_CONFIG.idea;
  const author = post.author || {};
  const authorName = author.name || "Acuité employee";

  return {
    id: `voice-post-${post.id}`,
    sourceId: post.id,
    title: post.title,
    body: post.body,
    topic,
    topicLabel: topicConfig.label,
    topicKicker: topicConfig.kicker,
    summary: topicConfig.summary,
    commentCount: post.comment_count || 0,
    authorName,
    authorMeta: [author.title, author.location].filter(Boolean).join(" | ") || author.email || "Employee",
    initials: author.initials || initialsFromName(authorName),
    avatar: gradientKeyFromText(`${authorName}-${topic}`),
    postedAtLabel: formatRelativeTime(post.published_at || post.created_at),
    createdAt: post.created_at || "",
    pinned: Boolean(post.pinned),
  };
}

function mapVoicePoll(poll) {
  return {
    ...poll,
    options: Array.isArray(poll.options)
      ? poll.options.map((option, index) => ({
        ...option,
        color: VOICE_POLL_OPTION_BACKGROUNDS[index % VOICE_POLL_OPTION_BACKGROUNDS.length],
      }))
      : [],
  };
}

function getFilteredCommunityPosts() {
  const posts = appData.communityPosts.slice().sort((left, right) => {
    return new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime();
  });
  if (state.communityFilter === "all") {
    return posts;
  }
  return posts.filter((post) => post.board === state.communityFilter);
}

function getFilteredVoicePosts() {
  const posts = appData.voicePosts.slice().sort((left, right) => {
    return new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime();
  });
  if (state.voiceFilter === "all") {
    return posts;
  }
  return posts.filter((post) => post.topic === state.voiceFilter);
}

function getFilteredLearningBooks() {
  const query = state.learningBookQuery.trim().toLowerCase();
  let books = appData.learningBooks.slice();

  if (state.learningBookFilter === "available") {
    books = books.filter((book) => book.available_copies > 0);
  } else if (state.learningBookFilter === "requested") {
    books = books.filter((book) => book.requester_has_open_requisition);
  }

  if (!query) {
    return books;
  }

  return books.filter((book) => {
    return [book.title, book.author, book.summary]
      .filter(Boolean)
      .join(" ")
      .toLowerCase()
      .includes(query);
  });
}

function summarizeCommunityCities() {
  const counts = new Map();
  appData.communityPosts.forEach((post) => {
    if (!post.city) {
      return;
    }
    const key = post.city.trim();
    if (!key) {
      return;
    }
    counts.set(key, (counts.get(key) || 0) + 1);
  });

  return [...counts.entries()]
    .sort((left, right) => right[1] - left[1] || left[0].localeCompare(right[0]))
    .slice(0, 4)
    .map(([city, count]) => ({
      city,
      count,
      note: count === 1 ? "1 live post" : `${count} live posts`,
    }));
}

function isOpenLearningStatus(status) {
  return ["requested", "approved", "issued"].includes(status);
}

function learningStatusLabel(status) {
  const labels = {
    requested: "Requested",
    approved: "Approved",
    issued: "Issued",
    returned: "Returned",
    declined: "Declined",
    cancelled: "Cancelled",
  };
  return labels[status] || capitalize(status);
}

function syncCommunityComposer() {
  if (!elements.communityBoardSelect || !elements.communityTypeSelect || !elements.communityMetaLabel || !elements.communityMetaInput) {
    return;
  }

  const board = elements.communityBoardSelect.value || "marketplace";
  const boardConfig = COMMUNITY_BOARD_CONFIG[board] || COMMUNITY_BOARD_CONFIG.marketplace;
  const previousType = elements.communityTypeSelect.value;

  elements.communityTypeSelect.innerHTML = boardConfig.types.map((type) => `
    <option value="${escapeHtml(type.value)}">${escapeHtml(type.label)}</option>
  `).join("");

  if (boardConfig.types.some((type) => type.value === previousType)) {
    elements.communityTypeSelect.value = previousType;
  }

  elements.communityMetaLabel.textContent = boardConfig.metaLabel;
  elements.communityMetaInput.placeholder = boardConfig.metaPlaceholder;
}

function syncVoiceComposer() {
  if (!elements.voiceTopicSelect) {
    return;
  }

  const options = appData.currentUser.is_staff
    ? ["idea", "csr", "ceo_corner"]
    : ["idea", "csr"];
  const previousValue = elements.voiceTopicSelect.value;

  elements.voiceTopicSelect.innerHTML = options.map((topic) => `
    <option value="${escapeHtml(topic)}">${escapeHtml(VOICE_TOPIC_CONFIG[topic].label)}</option>
  `).join("");

  if (options.includes(previousValue)) {
    elements.voiceTopicSelect.value = previousValue;
  }
}

async function submitVoicePost() {
  const formData = new FormData(elements.voiceForm);
  const topic = String(formData.get("topic") || "").trim();
  const title = String(formData.get("title") || "").trim();
  const body = String(formData.get("body") || "").trim();

  if (!topic || !title || !body) {
    showToast("Choose a channel, add a title and write the message before posting.");
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
      method: "POST",
      body: {
        title,
        body,
        module: "ideas_voice",
        topic,
      },
    });

    if (payload.post) {
      appData.voicePosts.unshift(mapVoicePost(payload.post));
      elements.voiceForm.reset();
      syncVoiceComposer();
      renderVoicePanel();
      renderPoll();
      showToast(
        payload.post.moderation_status === "published"
          ? "Post shared live in Ideas & Voice."
          : "Post submitted for review.",
      );
      return;
    }

    showToast("Ideas & Voice post created.");
  } catch (error) {
    showToast(error.message || "Could not post to Ideas & Voice.");
  }
}

async function voteOnPoll(optionId) {
  if (!appData.activePoll) {
    showToast("No active poll is running right now.");
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest(`/api/voice/polls/${appData.activePoll.id}/vote/`, {
      method: "POST",
      body: {
        option_id: Number(optionId),
      },
    });

    if (payload.poll) {
      appData.activePoll = mapVoicePoll(payload.poll);
      renderVoicePollCard();
      renderPoll();
      showToast("Your vote has been recorded.");
      return;
    }

    showToast("Vote recorded.");
  } catch (error) {
    showToast(error.message || "Could not record your vote.");
  }
}

function hydrateState() {
  const saved = readState();
  if (!saved) {
    return { ...defaultState };
  }

  return {
    ...defaultState,
    ...saved,
    communityFilter: (
      typeof saved.communityFilter === "string"
      && ["all", ...Object.keys(COMMUNITY_BOARD_CONFIG)].includes(saved.communityFilter)
    )
      ? saved.communityFilter
      : defaultState.communityFilter,
    voiceFilter: (
      typeof saved.voiceFilter === "string"
      && ["all", ...Object.keys(VOICE_TOPIC_CONFIG)].includes(saved.voiceFilter)
    )
      ? saved.voiceFilter
      : defaultState.voiceFilter,
    learningBookFilter: (
      typeof saved.learningBookFilter === "string"
      && ["all", "available", "requested"].includes(saved.learningBookFilter)
    )
      ? saved.learningBookFilter
      : defaultState.learningBookFilter,
    learningBookQuery: typeof saved.learningBookQuery === "string"
      ? saved.learningBookQuery
      : defaultState.learningBookQuery,
    directoryFilters: {
      ...createDirectoryFiltersState(),
      ...(saved.directoryFilters && typeof saved.directoryFilters === "object"
        ? Object.fromEntries(
          DIRECTORY_FILTER_GROUPS.map((groupId) => [
            groupId,
            normalizeDirectoryFilterSelections(saved.directoryFilters[groupId]),
          ]),
        )
        : {}),
    },
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

function createDirectoryFilterOptions() {
  return {
    company: [],
    location: [],
    department: [],
  };
}

function createDirectoryFiltersState() {
  return {
    company: [],
    location: [],
    department: [],
  };
}

function normalizeDirectoryFilterSelections(value) {
  if (Array.isArray(value)) {
    return value.filter((item) => typeof item === "string" && item.trim());
  }
  if (typeof value === "string" && value.trim() && value !== "all") {
    return [value];
  }
  return [];
}

function toggleDirectoryFilterSelection(selectedValues, value) {
  if (value === "all") {
    return [];
  }
  return toggleArrayValue(normalizeDirectoryFilterSelections(selectedValues), value);
}

function isDirectoryFilterOptionActive(selectedValues, value) {
  if (value === "all") {
    return !selectedValues.length;
  }
  return selectedValues.includes(value);
}

function displayCompanyName(value) {
  return COMPANY_DISPLAY_LABELS[value] || value;
}

function displayDirectoryFilterLabel(groupId, value) {
  if (groupId === "company") {
    return displayCompanyName(value);
  }
  return value;
}

function gradientValue(key) {
  return gradients[key] || gradients.warm;
}

function gradientKeyFromText(text) {
  const source = String(text || "acuite");
  const keys = Object.keys(gradients);
  const hash = [...source].reduce((total, character) => total + character.charCodeAt(0), 0);
  return keys[hash % keys.length];
}

function capitalize(value) {
  return value ? value.charAt(0).toUpperCase() + value.slice(1) : "";
}

function getCommunityBoardLabel(board) {
  return (COMMUNITY_BOARD_CONFIG[board] && COMMUNITY_BOARD_CONFIG[board].label) || "Community";
}

function getCommunityTypeLabel(board, type) {
  const boardConfig = COMMUNITY_BOARD_CONFIG[board];
  const match = boardConfig ? boardConfig.types.find((item) => item.value === type) : null;
  return match ? match.label : capitalize(String(type || "").replaceAll("_", " "));
}

function getVoiceTopicLabel(topic) {
  return (VOICE_TOPIC_CONFIG[topic] && VOICE_TOPIC_CONFIG[topic].label)
    || capitalize(String(topic || "").replaceAll("_", " "));
}

function formatDisplayDate(value) {
  if (!value) {
    return "";
  }
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return String(value);
  }
  return parsed.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function formatRelativeTime(value) {
  if (!value) {
    return "";
  }
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return String(value);
  }

  const diffMs = Date.now() - parsed.getTime();
  const diffMinutes = Math.max(1, Math.round(diffMs / 60000));
  if (diffMinutes < 60) {
    return `${diffMinutes} min ago`;
  }

  const diffHours = Math.round(diffMinutes / 60);
  if (diffHours < 24) {
    return `${diffHours} hr ago`;
  }

  const diffDays = Math.round(diffHours / 24);
  if (diffDays < 7) {
    return `${diffDays} day${diffDays === 1 ? "" : "s"} ago`;
  }

  return formatDisplayDate(value);
}

function directoryCardDetail(label, value) {
  if (!value) {
    return "";
  }
  return `
    <div class="person-detail-item">
      <span class="person-detail-label">${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
    </div>
  `;
}

function mapDirectoryProfileToCard(profile) {
  const company = profile.company_name || "";
  const companyLabel = displayCompanyName(company);
  const department = profile.department || "";
  const functionName = profile.function_name || "";
  const office = profile.office_location || profile.location || profile.city || "";
  const joinedOn = formatDisplayDate(profile.joined_on);
  const contactLine = [profile.email, profile.mobile_number || profile.phone_number].filter(Boolean).join(" | ");
  const teams = [companyLabel, department, functionName].filter(Boolean);

  return {
    id: `person-${profile.id}`,
    name: profile.name,
    initials: profile.initials || initialsFromName(profile.name),
    role: profile.title || "Employee",
    city: profile.city || office,
    company,
    companyLabel,
    department,
    functionName,
    office,
    officeLine: [office, companyLabel].filter(Boolean).join(" | "),
    employeeCode: profile.employee_code || "",
    joinedOn,
    contactLine,
    teams,
    skills: [],
    searchText: [
      profile.name,
      profile.email,
      profile.title,
      company,
      companyLabel,
      department,
      functionName,
      office,
      profile.location,
      profile.mobile_number,
      profile.employee_code,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase(),
    gradient: gradientKeyFromText(`${company}-${department}-${profile.name}`),
  };
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

function renderVoicePostCard(post) {
  return `
    <article class="card voice-card voice-topic-${escapeHtml(post.topic)}" id="${post.id}">
      <div class="voice-card-top">
        <div class="voice-card-tags">
          <span class="mini-chip">${escapeHtml(post.topicLabel)}</span>
          ${post.pinned ? `<span class="mini-chip success">Pinned</span>` : ""}
        </div>
        <div class="community-time">${escapeHtml(post.postedAtLabel)}</div>
      </div>
      <div class="card-header">
        <div class="card-avatar" style="background:${gradientValue(post.avatar)}">${escapeHtml(post.initials)}</div>
        <div class="card-meta">
          <div class="card-name">${escapeHtml(post.authorName)}</div>
          <div class="card-sub">${escapeHtml(post.authorMeta)}</div>
        </div>
      </div>
      <div class="card-body">
        <div class="card-title">${escapeHtml(post.title)}</div>
        <p>${escapeHtml(post.body)}</p>
      </div>
      <div class="card-actions">
        <button type="button" class="action-btn" data-action="placeholder-comment">
          ${commentIcon()}${escapeHtml(String(post.commentCount))}
        </button>
        <div class="spacer"></div>
        <button
          type="button"
          class="btn-outline"
          data-action="post-cta"
          data-message="${escapeHtml(`Open a discussion around this ${getVoiceTopicLabel(post.topic).toLowerCase()} post.`)}"
        >
          Discuss
        </button>
      </div>
    </article>
  `;
}

function renderPollOptions(poll) {
  if (!poll.options.length) {
    return `<div class="empty-state">Poll options are not configured yet.</div>`;
  }

  return poll.options.map((option) => {
    const voted = poll.user_vote_option_id === option.id;
    const disabled = !poll.is_open ? "disabled" : "";
    return `
      <button
        type="button"
        class="poll-option ${voted ? "voted" : ""}"
        data-action="vote-poll"
        data-id="${option.id}"
        ${disabled}
      >
        <div class="poll-bar" style="width:${option.percent}%;background:${option.color}"></div>
        <span class="poll-text">${escapeHtml(option.label)}</span>
        <span class="poll-pct">${escapeHtml(String(option.percent))}%</span>
      </button>
    `;
  }).join("");
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
