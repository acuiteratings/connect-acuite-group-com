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
const RECOGNITION_TOPIC_CONFIG = {
  kudos: {
    label: "Kudos",
    kicker: "Recognition",
    title: "Public appreciation for great work",
    summary: "Kudos posts should call out the work, the behavior and the impact so appreciation feels earned and useful.",
    tagLabel: "Recognition tag",
    emptyCopy: "The first live kudos post will appear here and begin shaping the tone of recognition inside Connect.",
    tags: [
      { value: "sharp_analysis", label: "Sharp analysis" },
      { value: "team_player", label: "Team player" },
      { value: "client_hero", label: "Client hero" },
      { value: "mentor", label: "Mentored me" },
      { value: "innovation", label: "Innovation" },
    ],
  },
  milestone: {
    label: "Milestones",
    kicker: "Celebration",
    title: "Work achievements and important moments",
    summary: "Milestones give important achievements, work anniversaries and notable employee moments a durable place inside the company story.",
    tagLabel: "Milestone type",
    emptyCopy: "Milestone posts will appear here once employees begin celebrating key achievements and work moments.",
    tags: [
      { value: "achievement", label: "Achievement" },
      { value: "work_anniversary", label: "Work anniversary" },
      { value: "birthday", label: "Birthday" },
      { value: "celebration", label: "Celebration" },
    ],
  },
};
const REWARD_RULE_LABELS = {
  published_post: "Post published",
  published_comment: "Comment posted",
  reaction_given: "Like given",
  reaction_received: "Like received",
};
const STORE_CATEGORY_LABELS = {
  apparel: "Apparel",
  drinkware: "Drinkware",
  desk: "Desk",
  memorabilia: "Memorabilia",
};
const BULLETIN_CATEGORY_LABELS = {
  announcements: "Announcements",
  hr: "HR",
  events: "Events",
  security: "Security",
};
const BULLETIN_TEMPLATE_LIBRARY = [
  {
    key: "town_hall",
    label: "Town Hall",
    category: "announcements",
    title: "Town hall | Leadership update and open Q&A",
    body:
      "We are hosting a company town hall to share key business updates, priorities for the coming quarter, and a live Q&A with leadership. Please block the time and join promptly.",
  },
  {
    key: "cybersecurity_warning",
    label: "Cybersecurity Warning",
    category: "security",
    title: "Cybersecurity advisory | Please review immediately",
    body:
      "A fresh cybersecurity advisory is being issued for all employees. Please review the guidance, avoid suspicious links or attachments, and report anything unusual to the IT team without delay.",
  },
  {
    key: "picnic",
    label: "Picnic",
    category: "events",
    title: "Company picnic | Save the date",
    body:
      "We are planning a company picnic for employees and would love broad participation. Venue, reporting time, transport details and participation instructions will follow shortly.",
  },
  {
    key: "office_party",
    label: "Office Party",
    category: "events",
    title: "Office party | Join the celebration",
    body:
      "We are getting together for an office celebration and would love everyone to join. Please block the evening, come ready to unwind, and watch this space for final timing and venue details.",
  },
  {
    key: "offsite",
    label: "Offsite",
    category: "events",
    title: "Team offsite | Planning note",
    body:
      "We are planning an upcoming offsite focused on collaboration, reflection and future priorities. Please indicate your availability once dates and logistics are shared.",
  },
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

const FEATURED_HOME_ANNOUNCEMENT = {
  id: "announcement-townhall-launch",
  eyebrow: "Priority Announcement",
  type: "Town Hall",
  format: "Hybrid",
  title: "Town hall and leadership briefing.",
  summary: "The next all-hands is being treated as a high-signal moment: a live walkthrough of Acuite Connect, a business update from leadership, and a focused Q&A on how we work together better from here.",
  dateLabel: "Thursday, 23rd April 2026",
  timeLabel: "4:00 PM - 5:30 PM IST",
  venueLabel: "Venue: TBD",
  hostLabel: "Hosted by the MD & CEO with the leadership team",
  audienceLabel: "Open to all employees",
  countdownLabel: "21 days to go",
  agenda: [
    "Acuite Connect launch and rollout note",
    "Business priorities and FY27 direction",
    "Open floor Q&A with leadership",
  ],
  outcomes: [
    "Reserve your seat or mark yourself as interested",
    "Block the time directly on your calendar",
    "Signal momentum through likes before the event",
  ],
  baseMetrics: {
    booked: 84,
    interested: 127,
    likes: 96,
  },
  calendar: {
    title: "Acuite Connect Launch Town Hall",
    description: "Acuite Connect launch walkthrough, business update, and leadership Q&A for all employees.",
    location: "Venue: TBD",
    start: "2026-04-23T16:00:00+05:30",
    end: "2026-04-23T17:30:00+05:30",
  },
};
const CONNECT_BOOT_USER_KEY = "acuite-connect-boot-user";

const appData = {
  currentUser: {
    name: "",
    initials: "",
    role: "",
    city: "",
    is_staff: false,
    accessLevel: "employee",
    accessRights: {
      can_employee: true,
      can_moderate: false,
      can_administer: false,
      can_manage_access_rights: false,
      can_post: true,
      can_comment: true,
      can_react: true,
      can_post_as_company: false,
    },
  },
  currentProfile: null,
  profileSkillLibrary: [],
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
      message: "Help Desk is staged as a planned module in the current Connect foundation.",
    },
  ],
  communityPosts: [],
  voicePosts: [],
  recognitionPosts: [],
  activePoll: null,
  currentUserPoints: 0,
  rewardRules: [],
  recognitionTotals: {},
  storeItems: [],
  storeRedemptions: [],
  storeBalance: {
    earned_points: 0,
    locked_points: 0,
    available_points: 0,
  },
  adminUsers: [],
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
        "This is an early practical workspace pass for Connect. Please explore the new directory, tool hub, and knowledge sections.",
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
  currentProfile: null,
  profileSkillLibrary: [],
  agenda: [],
  tasks: [],
  pulse: [],
  communityPosts: [],
  voicePosts: [],
  recognitionPosts: [],
  activePoll: null,
  currentUserPoints: 0,
  rewardRules: [],
  recognitionTotals: {},
  storeItems: [],
  storeRedemptions: [],
  storeBalance: {
    earned_points: 0,
    locked_points: 0,
    available_points: 0,
  },
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
  recognitionFilter: "all",
  storeFilter: "all",
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
  homeAnnouncementLiked: false,
  homeAnnouncementInterested: false,
  homeAnnouncementBooked: false,
  homeAnnouncementCalendarBlocked: false,
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
let recognitionLoadError = "";
let storeLoadError = "";
let learningLoadError = "";
let bulletinLoadError = "";
let adminUsersLoadError = "";
let profileBuilderLoadError = "";
let profileBuilderDraft = createProfileBuilderDraft();
let profileMenuOpen = false;
let activeCommentsPostId = 0;
let liveComments = [];
let liveCommentsError = "";
let liveCommentsLoading = false;
let selectedAdminUserId = null;
let selectedBulletinTemplateKey = BULLETIN_TEMPLATE_LIBRARY[0].key;

document.addEventListener("DOMContentLoaded", () => {
  void init();
});

function markAppReady() {
  document.body.classList.remove("connect-app-loading");
}

function mergeAuthenticatedUser(user) {
  if (!user) {
    return;
  }
  appData.currentUser = {
    ...appData.currentUser,
    ...user,
    role: user.title || appData.currentUser.role,
    city: user.location || appData.currentUser.city,
    is_staff: Boolean(user.is_staff),
    accessLevel: user.access_level || appData.currentUser.accessLevel,
    accessRights: {
      ...appData.currentUser.accessRights,
      ...(user.access_rights || {}),
    },
  };
  if (!appData.currentUser.initials && appData.currentUser.name) {
    appData.currentUser.initials = initialsFromName(appData.currentUser.name);
  }
}

function consumeBootSession() {
  try {
    const raw = window.sessionStorage.getItem(CONNECT_BOOT_USER_KEY);
    if (!raw) {
      return null;
    }
    window.sessionStorage.removeItem(CONNECT_BOOT_USER_KEY);
    const payload = JSON.parse(raw);
    if (!payload || !payload.created_at) {
      return null;
    }
    if (Date.now() - Number(payload.created_at) > 120000) {
      return null;
    }
    if (payload.session && payload.session.user) {
      return payload.session;
    }
    if (payload.user) {
      return {
        authenticated: true,
        user: payload.user,
      };
    }
    return null;
  } catch (error) {
    return null;
  }
}

function renderShell() {
  renderPanels();
  renderProfile();
  renderProfileBuilder();
  renderCommentsModal();
  syncComposerAccess();
  renderHomeAnnouncement();
  renderTodayPanel();
  renderTasksPanel();
  renderPulsePanel();
  renderHomeTools();
  renderHomeFeed();
  renderBirthdays();
  renderAnniversaries();
  renderUpcoming();
  renderPoll();
  renderSavedResources();
}

async function init() {
  const bootSession = consumeBootSession();
  const bootUser = bootSession ? bootSession.user : null;
  if (bootUser) {
    mergeAuthenticatedUser(bootUser);
    if (window.AcuiteConnectAuth && window.AcuiteConnectAuth.hydrateSession) {
      window.AcuiteConnectAuth.hydrateSession(bootSession);
    }
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
    adminSidebarTab: document.getElementById("admin-sidebar-tab"),
    bulletinAdminOpenButton: document.getElementById("bulletin-admin-open-btn"),
    adminCreateUserForm: document.getElementById("admin-create-user-form"),
    adminEditUserForm: document.getElementById("admin-edit-user-form"),
    adminBulletinForm: document.getElementById("admin-bulletin-form"),
    adminUserSearchInput: document.getElementById("admin-user-search"),
    adminUserList: document.getElementById("admin-user-list"),
    adminUserResultsMeta: document.getElementById("admin-user-results-meta"),
    adminEditUserId: document.getElementById("admin-edit-user-id"),
    adminEditDisplayName: document.getElementById("admin-edit-display-name"),
    adminEditEmail: document.getElementById("admin-edit-email"),
    adminEditTitle: document.getElementById("admin-edit-title"),
    adminEditDepartment: document.getElementById("admin-edit-department"),
    adminEditLocation: document.getElementById("admin-edit-location"),
    adminEditCode: document.getElementById("admin-edit-code"),
    adminEditAccessLevel: document.getElementById("admin-edit-access-level"),
    adminEditEmploymentStatus: document.getElementById("admin-edit-employment-status"),
    adminEditCanPost: document.getElementById("admin-edit-can-post"),
    adminEditIsActive: document.getElementById("admin-edit-is-active"),
    adminEditStatus: document.getElementById("admin-edit-status"),
    adminEditSubmit: document.getElementById("admin-edit-submit"),
    adminBulletinTemplates: document.getElementById("admin-bulletin-templates"),
    voiceForm: document.getElementById("voice-form"),
    voiceTopicSelect: document.getElementById("voice-topic-select"),
    recognitionForm: document.getElementById("recognition-form"),
    recognitionTopicSelect: document.getElementById("recognition-topic-select"),
    recognitionTagSelect: document.getElementById("recognition-tag-select"),
    recognitionTagLabel: document.getElementById("recognition-tag-label"),
    recognitionRecipientSelect: document.getElementById("recognition-recipient-select"),
    bulletinForm: document.getElementById("bulletin-form"),
    kudosForm: document.getElementById("kudos-form"),
    pitchForm: document.getElementById("pitch-form"),
    profileBuilderForm: document.getElementById("profile-builder-form"),
    profileMenu: document.getElementById("profile-menu"),
    profileMenuAdminLink: document.getElementById("profile-menu-admin-link"),
    profileModalBackdrop: document.getElementById("profile-modal-backdrop"),
    commentsModalBackdrop: document.getElementById("comments-modal-backdrop"),
    commentsModalList: document.getElementById("comments-modal-list"),
    commentsModalMeta: document.getElementById("comments-modal-meta"),
    commentsModalForm: document.getElementById("comments-modal-form"),
    commentsModalInput: document.getElementById("comments-modal-input"),
    commentsModalStatus: document.getElementById("comments-modal-status"),
    profilePhotoInputOne: document.getElementById("profile-photo-input-1"),
    profilePhotoInputTwo: document.getElementById("profile-photo-input-2"),
    profilePhotoPreviewGrid: document.getElementById("profile-photo-preview-grid"),
    profileSkillLibrary: document.getElementById("profile-skill-library"),
    profileHobbiesInput: document.getElementById("profile-hobbies-input"),
    profileInterestsInput: document.getElementById("profile-interests-input"),
    profileBuilderStatus: document.getElementById("profile-builder-status"),
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
  renderShell();
  if (bootUser) {
    markAppReady();
  }

  const authenticatedUser = window.AcuiteConnectAuth && window.AcuiteConnectAuth.requireAuth
    ? await window.AcuiteConnectAuth.requireAuth({ loginPath: "/login.html" })
    : null;
  if (window.AcuiteConnectAuth && !authenticatedUser) {
    return;
  }
  mergeAuthenticatedUser(authenticatedUser);
  renderShell();
  markAppReady();

  try {
    const criticalTasks = [
      loadCurrentProfile(),
      loadVoiceData(),
      loadRecognitionData(),
      loadBulletinPosts(),
    ];
    await Promise.allSettled(criticalTasks);
    renderAll();
    void Promise.allSettled([
      loadDirectoryData(),
      loadCommunityPosts(),
      loadStoreData(),
      loadLearningData(),
    ]).then(() => {
      renderAll();
    });
  } catch (error) {
    console.error("Could not complete the initial Connect render.", error);
    renderAll();
  }
}

async function loadCurrentProfile() {
  profileBuilderLoadError = "";
  appData.currentProfile = null;
  appData.profileSkillLibrary = [];

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    profileBuilderLoadError = "Profile builder is unavailable in this build.";
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/directory/me/");
    appData.currentProfile = payload.profile || null;
    appData.profileSkillLibrary = Array.isArray(payload.skill_library) ? payload.skill_library : [];
    profileBuilderDraft = createProfileDraftFromProfile(appData.currentProfile);
  } catch (error) {
    profileBuilderLoadError = error.message || "Could not load your profile builder.";
  }
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

async function loadRecognitionData() {
  recognitionLoadError = "";
  appData.recognitionPosts = [];

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    recognitionLoadError = "Recognition services are unavailable in this build.";
    return;
  }

  try {
    const [postsPayload, overviewPayload] = await Promise.all([
      window.AcuiteConnectAuth.apiRequest("/api/feed/posts/?module=recognition"),
      window.AcuiteConnectAuth.apiRequest("/api/recognition/overview/"),
    ]);
    appData.recognitionPosts = Array.isArray(postsPayload.results)
      ? postsPayload.results.map(mapRecognitionPost)
      : [];
    appData.leaderboard = Array.isArray(overviewPayload.leaderboard)
      ? overviewPayload.leaderboard
      : [];
    appData.birthdays = Array.isArray(overviewPayload.birthdays)
      ? overviewPayload.birthdays
      : [];
    appData.anniversaries = Array.isArray(overviewPayload.anniversaries)
      ? overviewPayload.anniversaries
      : [];
    appData.currentUserPoints = Number(overviewPayload.current_user_points || 0);
    appData.rewardRules = Array.isArray(overviewPayload.point_rules)
      ? overviewPayload.point_rules
      : [];
    appData.recognitionTotals = overviewPayload.totals || {};
  } catch (error) {
    recognitionLoadError = error.message || "Could not load Recognition & Rewards.";
    appData.leaderboard = [];
    appData.birthdays = [];
    appData.anniversaries = [];
    appData.currentUserPoints = 0;
    appData.rewardRules = [];
    appData.recognitionTotals = {};
  }
}

async function loadStoreData() {
  storeLoadError = "";
  appData.storeItems = [];
  appData.storeRedemptions = [];
  appData.storeBalance = {
    earned_points: 0,
    locked_points: 0,
    available_points: 0,
  };

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    storeLoadError = "Brand Store services are unavailable in this build.";
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/store/overview/");
    appData.storeItems = Array.isArray(payload.items) ? payload.items : [];
    appData.storeRedemptions = Array.isArray(payload.my_redemptions) ? payload.my_redemptions : [];
    appData.storeBalance = payload.balance || appData.storeBalance;
  } catch (error) {
    storeLoadError = error.message || "Could not load the Brand Store.";
  }
}

async function loadBulletinPosts() {
  bulletinLoadError = "";
  appData.bulletinPosts = [];

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    bulletinLoadError = "Bulletin services are unavailable in this build.";
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/?module=general&kind=announcement");
    appData.bulletinPosts = Array.isArray(payload.results)
      ? payload.results.map(mapBulletinPost)
      : [];
  } catch (error) {
    bulletinLoadError = error.message || "Could not load the Bulletin Board.";
  }
}

async function loadAdminUsers() {
  adminUsersLoadError = "";
  appData.adminUsers = [];

  if (!currentUserCanAdministerConnect()) {
    return;
  }
  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    adminUsersLoadError = "Admin services are unavailable in this build.";
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/accounts/access/users/");
    appData.adminUsers = Array.isArray(payload.results) ? payload.results : [];
  } catch (error) {
    adminUsersLoadError = error.message || "Could not load employee admin tools.";
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

  if (elements.recognitionTopicSelect) {
    elements.recognitionTopicSelect.addEventListener("change", () => {
      syncRecognitionComposer();
    });
  }

  if (elements.learningBookSearchInput) {
    elements.learningBookSearchInput.addEventListener("input", (event) => {
      state.learningBookQuery = event.target.value;
      saveState();
      renderLearningPanel();
    });
  }

  if (elements.adminUserSearchInput) {
    elements.adminUserSearchInput.addEventListener("input", () => {
      renderAdminUserList();
    });
  }

  elements.directorySearchInput.addEventListener("input", (event) => {
    state.directoryQuery = event.target.value;
    saveState();
    renderDirectory();
  });

  if (elements.profileHobbiesInput) {
    elements.profileHobbiesInput.addEventListener("input", (event) => {
      profileBuilderDraft.hobbiesText = event.target.value;
    });
  }

  if (elements.profileInterestsInput) {
    elements.profileInterestsInput.addEventListener("input", (event) => {
      profileBuilderDraft.interestsText = event.target.value;
    });
  }

  if (elements.profilePhotoInputOne) {
    elements.profilePhotoInputOne.addEventListener("change", (event) => {
      void handleProfilePhotoSelection(event, 0);
    });
  }

  if (elements.profilePhotoInputTwo) {
    elements.profilePhotoInputTwo.addEventListener("change", (event) => {
      void handleProfilePhotoSelection(event, 1);
    });
  }
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

    if (actionName === "book-home-announcement") {
      state.homeAnnouncementBooked = !state.homeAnnouncementBooked;
      if (state.homeAnnouncementBooked) {
        state.homeAnnouncementInterested = true;
      }
      saveState();
      renderHomeAnnouncement();
      showToast(state.homeAnnouncementBooked ? "Your seat is booked." : "Your booking has been removed.");
      return;
    }

    if (actionName === "block-home-announcement") {
      downloadAnnouncementCalendarInvite();
      state.homeAnnouncementCalendarBlocked = true;
      saveState();
      renderHomeAnnouncement();
      showToast("Calendar block downloaded.");
      return;
    }

    if (actionName === "interest-home-announcement") {
      state.homeAnnouncementInterested = !state.homeAnnouncementInterested;
      saveState();
      renderHomeAnnouncement();
      showToast(state.homeAnnouncementInterested ? "Marked as interested." : "Interest removed.");
      return;
    }

    if (actionName === "like-home-announcement") {
      state.homeAnnouncementLiked = !state.homeAnnouncementLiked;
      saveState();
      renderHomeAnnouncement();
      showToast(state.homeAnnouncementLiked ? "Announcement liked." : "Like removed.");
      return;
    }

    if (actionName === "logout") {
      closeProfileMenu();
      if (window.AcuiteConnectAuth && window.AcuiteConnectAuth.logout) {
        await window.AcuiteConnectAuth.logout();
      }
      window.location.href = "/login.html";
      return;
    }

    if (actionName === "toggle-profile-menu") {
      toggleProfileMenu();
      return;
    }

    if (actionName === "open-profile-builder") {
      closeProfileMenu();
      openProfileBuilder();
      return;
    }

    if (actionName === "open-admin-console") {
      closeProfileMenu();
      window.location.href = "/admin-console.html";
      return;
    }

    if (actionName === "close-profile-builder") {
      closeProfileBuilder();
      return;
    }

    if (actionName === "open-live-comments") {
      await openLiveComments(action.dataset.id);
      return;
    }

    if (actionName === "close-live-comments") {
      closeLiveComments();
      return;
    }

    if (actionName === "toggle-profile-skill") {
      toggleProfileSkill(action.dataset.skill);
      return;
    }

    if (actionName === "clear-profile-photo") {
      clearProfilePhoto(Number(action.dataset.index));
      return;
    }

    if (actionName === "select-admin-user") {
      selectedAdminUserId = Number(action.dataset.id);
      renderAdminPanel();
      return;
    }

    if (actionName === "apply-bulletin-template") {
      applyBulletinTemplate(action.dataset.templateKey);
      return;
    }

    if (actionName === "toggle-like") {
      state.likedPostIds = toggleArrayValue(state.likedPostIds, action.dataset.id);
      saveState();
      renderAll();
      return;
    }

    if (actionName === "toggle-live-reaction") {
      await toggleLiveReaction(action.dataset.id);
      return;
    }

    if (actionName === "delete-live-post") {
      await deleteLivePost(action.dataset.id, action.dataset.module);
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

    if (actionName === "redeem-store-item") {
      await redeemStoreItem(action.dataset.id);
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
      showToast("Alumni invitations are staged as a future step for Connect.");
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

    if (actionName === "open-bulletin-cta") {
      const target = String(action.dataset.target || "").trim();
      if (!target) {
        showToast("This action is not available yet.");
        return;
      }
      if (target.startsWith("mailto:")) {
        window.location.href = target;
        return;
      }
      window.open(target, "_blank", "noopener,noreferrer");
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
    closeProfileMenu();
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

  if (elements.profileModalBackdrop && event.target === elements.profileModalBackdrop) {
    closeProfileBuilder();
  }

  if (elements.commentsModalBackdrop && event.target === elements.commentsModalBackdrop) {
    closeLiveComments();
  }

  if (!event.target.closest(".profile-menu-shell")) {
    closeProfileMenu();
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

  if (event.target === elements.recognitionForm) {
    event.preventDefault();
    void submitRecognitionPost();
    return;
  }

  if (event.target === elements.adminCreateUserForm) {
    event.preventDefault();
    void submitAdminCreateUser();
    return;
  }

  if (event.target === elements.adminEditUserForm) {
    event.preventDefault();
    void submitAdminEditUser();
    return;
  }

  if (event.target === elements.adminBulletinForm) {
    event.preventDefault();
    void submitAdminBulletinPost();
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
    return;
  }

  if (event.target === elements.profileBuilderForm) {
    event.preventDefault();
    void saveProfileBuilder();
    return;
  }

  if (event.target === elements.commentsModalForm) {
    event.preventDefault();
    void submitLiveComment();
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
  renderProfileBuilder();
  renderCommentsModal();
  syncComposerAccess();
  renderHomeAnnouncement();
  renderTodayPanel();
  renderTasksPanel();
  renderPulsePanel();
  renderHomeTools();
  renderHomeFeed();
  renderCommunityPanel();
  renderVoicePanel();
  renderRecognitionPanel();
  renderStorePanel();
  renderLearningPanel();
  renderBulletinPanel();
  renderAdminPanel();
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

function currentUserAccessRights() {
  return {
    can_employee: true,
    can_moderate: false,
    can_administer: false,
    can_manage_access_rights: false,
    can_post: true,
    can_comment: true,
    can_react: true,
    can_post_as_company: false,
    ...(appData.currentUser.accessRights || {}),
  };
}

function currentUserCanCreatePosts() {
  return Boolean(currentUserAccessRights().can_post);
}

function currentUserCanAdministerConnect() {
  return Boolean(currentUserAccessRights().can_administer);
}

function renderPanels() {
  const canAdminister = currentUserCanAdministerConnect();
  const activeSidebarTab = state.activeTab === "battleship" ? "playtime" : state.activeTab;
  if (state.activeTab === "admin") {
    state.activeTab = "home";
    saveState();
  }
  document.documentElement.setAttribute("data-theme", state.theme);
  const adminPanel = document.getElementById("panel-admin");
  if (elements.adminSidebarTab) {
    elements.adminSidebarTab.hidden = !canAdminister;
  }
  if (elements.bulletinAdminOpenButton) {
    elements.bulletinAdminOpenButton.hidden = !canAdminister;
  }
  if (adminPanel) {
    adminPanel.hidden = !canAdminister;
  }
  document.querySelectorAll(".panel").forEach((panel) => {
    panel.classList.toggle("active", panel.id === `panel-${state.activeTab}`);
  });
  document.querySelectorAll(".sidebar-left .tab").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.switchTab === activeSidebarTab);
  });
}

function renderProfile() {
  const canAdminister = currentUserCanAdministerConnect();
  const receivedKudos = state.customKudos.filter((item) => item.recipient.toLowerCase() === appData.currentUser.name.toLowerCase()).length
    + appData.recognitionPosts.filter((item) => item.topic === "kudos" && item.recipientUserId === appData.currentUser.id).length;
  const joinedClubs = state.joinedClubIds.length;
  const pitchesByRahul = appData.pitches.filter((item) => item.author === appData.currentUser.name).length + state.customPitches.length;

  setAvatarElement(elements.navAvatar, {
    initials: appData.currentUser.initials,
    gradient: "warm",
    photoUrl: appData.currentProfile?.profile_photos?.[0] || "",
  });
  elements.navAvatar.setAttribute("aria-expanded", profileMenuOpen ? "true" : "false");
  if (elements.composeAvatar) {
    elements.composeAvatar.textContent = appData.currentUser.initials;
  }
  setAvatarElement(elements.profileAvatar, {
    initials: appData.currentUser.initials,
    gradient: "warm",
    photoUrl: appData.currentProfile?.profile_photos?.[0] || "",
  });
  elements.profileName.textContent = appData.currentUser.name;
  elements.profileRole.textContent = appData.currentUser.role;
  elements.profileKudos.textContent = String(receivedKudos);
  elements.profileClubs.textContent = String(joinedClubs);
  elements.profilePitches.textContent = String(pitchesByRahul);
  if (elements.profileMenu) {
    elements.profileMenu.hidden = !profileMenuOpen;
  }
  if (elements.profileMenuAdminLink) {
    elements.profileMenuAdminLink.hidden = !canAdminister;
  }
}

function renderProfileBuilder() {
  if (!elements.profileBuilderForm) {
    return;
  }

  elements.profileBuilderForm.classList.toggle("is-disabled", Boolean(profileBuilderLoadError));
  if (elements.profileHobbiesInput) {
    elements.profileHobbiesInput.value = profileBuilderDraft.hobbiesText;
  }
  if (elements.profileInterestsInput) {
    elements.profileInterestsInput.value = profileBuilderDraft.interestsText;
  }

  if (elements.profilePhotoPreviewGrid) {
    const photos = profileBuilderDraft.photos;
    elements.profilePhotoPreviewGrid.innerHTML = [0, 1].map((index) => {
      const photo = photos[index] || "";
      return `
        <div class="profile-photo-card ${photo ? "has-photo" : ""}">
          ${
            photo
              ? `<img src="${escapeHtml(photo)}" alt="Profile photo ${index + 1}">`
              : `<div class="profile-photo-placeholder">Photo ${index + 1}</div>`
          }
          ${
            photo
              ? `<button type="button" class="btn-link profile-photo-clear" data-action="clear-profile-photo" data-index="${index}">Remove</button>`
              : ""
          }
        </div>
      `;
    }).join("");
  }

  if (elements.profileSkillLibrary) {
    elements.profileSkillLibrary.innerHTML = appData.profileSkillLibrary.length
      ? appData.profileSkillLibrary.map((skill) => `
          <button
            type="button"
            class="profile-skill-chip ${profileBuilderDraft.skills.includes(skill) ? "active" : ""}"
            data-action="toggle-profile-skill"
            data-skill="${escapeHtml(skill)}"
          >
            ${escapeHtml(skill)}
          </button>
        `).join("")
      : `<div class="mini-item-meta">Skill library is loading...</div>`;
  }

  if (elements.profileBuilderStatus) {
    elements.profileBuilderStatus.textContent = profileBuilderLoadError
      ? profileBuilderLoadError
      : "Add up to 2 photos, choose up to 10 skills, and tell colleagues what you enjoy.";
  }
}

function findLivePostById(postId) {
  const targetId = Number(postId || 0);
  if (!targetId) {
    return null;
  }
  const allPosts = [
    ...appData.communityPosts,
    ...appData.voicePosts,
    ...appData.recognitionPosts,
    ...appData.bulletinPosts,
  ];
  return allPosts.find((post) => Number(post.sourceId) === targetId) || null;
}

async function openLiveComments(postId) {
  const numericPostId = Number(postId || 0);
  if (!numericPostId || !window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    showToast("Comments are unavailable right now.");
    return;
  }

  activeCommentsPostId = numericPostId;
  liveCommentsLoading = true;
  liveCommentsError = "";
  liveComments = [];
  renderCommentsModal();

  if (elements.commentsModalBackdrop) {
    elements.commentsModalBackdrop.hidden = false;
  }
  document.body.classList.add("modal-open");

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest(`/api/feed/posts/${numericPostId}/comments/`);
    liveComments = Array.isArray(payload.results) ? payload.results : [];
  } catch (error) {
    liveCommentsError = error.message || "Could not load comments for this post.";
  } finally {
    liveCommentsLoading = false;
    renderCommentsModal();
  }
}

function closeLiveComments() {
  activeCommentsPostId = 0;
  liveComments = [];
  liveCommentsError = "";
  liveCommentsLoading = false;
  if (elements.commentsModalBackdrop) {
    elements.commentsModalBackdrop.hidden = true;
  }
  document.body.classList.remove("modal-open");
}

function renderCommentsModal() {
  if (!elements.commentsModalBackdrop || !elements.commentsModalList || !elements.commentsModalMeta) {
    return;
  }

  if (!activeCommentsPostId) {
    elements.commentsModalBackdrop.hidden = true;
    return;
  }

  const post = findLivePostById(activeCommentsPostId);
  elements.commentsModalBackdrop.hidden = false;
  elements.commentsModalMeta.textContent = post
    ? `${post.title} | ${post.authorName}`
    : "Loading discussion...";
  const commentingAllowed = currentUserAccessRights().can_comment && Boolean(post?.allowComments ?? true);

  if (elements.commentsModalStatus) {
    elements.commentsModalStatus.textContent = !currentUserAccessRights().can_comment
      ? "Commenting is disabled for this account."
      : !Boolean(post?.allowComments ?? true)
        ? "Comments are disabled for this post."
        : "Comments are posted live for colleagues.";
  }
  if (elements.commentsModalInput) {
    elements.commentsModalInput.disabled = !commentingAllowed;
  }
  const submitButton = elements.commentsModalForm?.querySelector('button[type="submit"]');
  if (submitButton) {
    submitButton.disabled = !commentingAllowed;
  }

  if (liveCommentsLoading) {
    elements.commentsModalList.innerHTML = '<div class="empty-state">Loading comments...</div>';
    return;
  }

  if (liveCommentsError) {
    elements.commentsModalList.innerHTML = `<div class="empty-state">${escapeHtml(liveCommentsError)}</div>`;
    return;
  }

  if (!liveComments.length) {
    elements.commentsModalList.innerHTML = '<div class="empty-state">No comments yet. Be the first to respond.</div>';
    return;
  }

  elements.commentsModalList.innerHTML = liveComments.map((comment) => `
    <article class="comments-modal-item">
      <div class="comments-modal-item-head">
        <strong>${escapeHtml(comment.author?.name || comment.author?.email || "Employee")}</strong>
        <span>${escapeHtml(formatRelativeTime(comment.created_at))}</span>
      </div>
      <div class="comments-modal-item-meta">${escapeHtml([comment.author?.title, comment.author?.location].filter(Boolean).join(" | "))}</div>
      <p>${escapeHtml(comment.body || "")}</p>
    </article>
  `).join("");
}

async function submitLiveComment() {
  if (!activeCommentsPostId) {
    showToast("Open a post before submitting a comment.");
    return;
  }
  const livePost = findLivePostById(activeCommentsPostId);
  if (!currentUserAccessRights().can_comment) {
    showToast("Commenting is disabled for this account.");
    return;
  }
  if (livePost && livePost.allowComments === false) {
    showToast("Comments are disabled for this post.");
    return;
  }
  const body = String(elements.commentsModalInput?.value || "").trim();
  if (!body) {
    showToast("Write a comment before posting.");
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest(`/api/feed/posts/${activeCommentsPostId}/comments/`, {
      method: "POST",
      body: { body },
    });
    if (elements.commentsModalInput) {
      elements.commentsModalInput.value = "";
    }
    if (payload.comment) {
      liveComments.push(payload.comment);
    }
    if (livePost) {
      livePost.commentCount += 1;
    }
    renderCommentsModal();
    renderAll();
    showToast("Comment posted.");
  } catch (error) {
    showToast(error.message || "Could not post the comment.");
  }
}

function syncComposerAccess() {
  const canCreatePosts = currentUserCanCreatePosts();
  [
    elements.communityForm,
    elements.voiceForm,
    elements.recognitionForm,
    elements.bulletinForm,
    elements.kudosForm,
    elements.pitchForm,
  ].forEach((form) => {
    setComposerAccessState(form, canCreatePosts);
  });
}

function setComposerAccessState(form, canCreatePosts) {
  if (!form) {
    return;
  }

  form.classList.toggle("is-disabled", !canCreatePosts);
  form.querySelectorAll("input, textarea, select, button").forEach((control) => {
    control.disabled = !canCreatePosts;
  });

  const actionsContainer = form.querySelector(".form-actions");
  let note = form.querySelector(".composer-access-note");
  if (!canCreatePosts) {
    if (!note) {
      note = document.createElement("p");
      note.className = "composer-access-note";
      if (actionsContainer) {
        actionsContainer.prepend(note);
      } else {
        form.prepend(note);
      }
    }
    note.textContent = "Your posting access is currently disabled. An admin can restore it.";
  } else if (note) {
    note.remove();
  }
}

function renderHomeAnnouncement() {
  const container = document.getElementById("home-announcement");
  if (!container) {
    return;
  }

  const announcement = FEATURED_HOME_ANNOUNCEMENT;
  container.innerHTML = `
    <div class="announcement-main">
      <div class="announcement-topline">
        <p class="eyebrow">${escapeHtml(announcement.eyebrow)}</p>
        <div class="announcement-badges">
          <span class="announcement-badge strong">${escapeHtml(announcement.type)}</span>
          <span class="announcement-badge">${escapeHtml(announcement.format)}</span>
          <span class="announcement-badge">${escapeHtml(announcement.dateLabel)}</span>
        </div>
      </div>

      <h1 class="announcement-title">${escapeHtml(announcement.title)}</h1>
      <p class="announcement-summary">${escapeHtml(announcement.summary)}</p>

      <div class="announcement-meta-grid">
        <article class="announcement-meta-card">
          <span class="announcement-meta-label">When</span>
          <strong>${escapeHtml(announcement.timeLabel)}</strong>
          <span>${escapeHtml(announcement.dateLabel)}</span>
        </article>
        <article class="announcement-meta-card">
          <span class="announcement-meta-label">Where</span>
          <strong>${escapeHtml(announcement.venueLabel)}</strong>
          <span>${escapeHtml(announcement.audienceLabel)}</span>
        </article>
        <article class="announcement-meta-card">
          <span class="announcement-meta-label">Hosted by</span>
          <strong>${escapeHtml(announcement.hostLabel)}</strong>
          <span>${escapeHtml(announcement.countdownLabel)}</span>
        </article>
      </div>
    </div>
    <div class="announcement-side announcement-side-actions">
      <button type="button" class="announcement-side-button" data-switch-tab="ideas-voice">Post a Question</button>
      <button type="button" class="announcement-side-button" data-switch-tab="ideas-voice">Share an Idea</button>
      <button type="button" class="announcement-side-button" data-switch-tab="ideas-voice">Give a Suggestion</button>
    </div>
  `;
}

function renderTodayPanel() {
  if (!document.getElementById("today-panel")) {
    return;
  }
  renderHomePillar("today-panel", HOME_PILLARS[0]);
}

function renderTasksPanel() {
  if (!document.getElementById("tasks-panel")) {
    return;
  }
  renderHomePillar("tasks-panel", HOME_PILLARS[1]);
}

function renderPulsePanel() {
  if (!document.getElementById("pulse-panel")) {
    return;
  }
  renderHomePillar("pulse-panel", HOME_PILLARS[2]);
}

function renderHomeTools() {
  const head = document.getElementById("home-core-spaces-head");
  const grid = document.getElementById("home-tools-grid");
  if (!head || !grid) {
    return;
  }
  if (head) {
    head.innerHTML = `
      <div>
        <p class="widget-kicker">Core Spaces</p>
        <h2>Explore the main employee spaces inside Connect</h2>
      </div>
      <button type="button" class="btn-link" data-switch-tab="community">Start exploring</button>
    `;
  }
  grid.innerHTML = HOME_CORE_SPACES.map(renderHomeSpaceCard).join("");
}

function renderHomeFeed() {
  const head = document.getElementById("home-foundation-head");
  const feed = document.getElementById("home-feed");
  if (!head || !feed) {
    return;
  }
  if (head) {
    head.innerHTML = `
      <div>
        <p class="widget-kicker">Foundation Layers</p>
        <h2>People, tools and knowledge behind every module</h2>
      </div>
      <button type="button" class="btn-link" data-switch-tab="directory">Open directory</button>
    `;
  }
  feed.innerHTML = HOME_FOUNDATION_LAYERS.map((layer) => `
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

function renderRecognitionPanel() {
  syncRecognitionComposer();
  renderRecognitionSummary();
  renderRecognitionFeed();
  renderRecognitionLeaderboardCard();
  renderRecognitionCelebrationsCard();
  renderRecognitionRewardsCard();
}

function renderStorePanel() {
  renderStoreSummary();
  renderStoreCatalog();
  renderStoreBalanceCard();
  renderStoreRedemptionsCard();
  renderStorePolicyCard();
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

function renderRecognitionSummary() {
  const filteredPosts = getFilteredRecognitionPosts();
  const totals = appData.recognitionTotals || {};
  const kudosCount = totals.kudos_posts || 0;
  const milestoneCount = totals.milestone_posts || 0;
  const topLeader = appData.leaderboard[0];

  document.getElementById("recognition-summary-grid").innerHTML = [
    {
      kicker: "Recognition",
      title: `${totals.recognition_posts || 0} live posts`,
      copy: "Appreciation and celebration posts that are now visible across the employee network.",
    },
    {
      kicker: "Kudos",
      title: `${kudosCount} kudos`,
      copy: "Public recognition for effort, teamwork, client impact, mentoring and analytical excellence.",
    },
    {
      kicker: "Milestones",
      title: `${milestoneCount} celebrations`,
      copy: "Work moments and achievements that deserve more than a passing mention.",
    },
    {
      kicker: "Rewards",
      title: topLeader && topLeader.points > 0 ? `${topLeader.points} pts` : `${appData.currentUserPoints} pts`,
      copy: topLeader && topLeader.points > 0
        ? `${topLeader.name} currently leads the engagement table.`
        : "Reward points begin to accumulate through posts, comments and likes.",
    },
  ].map((item) => `
    <article class="mini-panel">
      <p class="widget-kicker">${escapeHtml(item.kicker)}</p>
      <h3>${escapeHtml(item.title)}</h3>
      <p class="muted-copy">${escapeHtml(item.copy)}</p>
    </article>
  `).join("");

  document.getElementById("recognition-results-meta").textContent = appData.recognitionPosts.length
    ? `${filteredPosts.length} of ${appData.recognitionPosts.length} live recognition posts shown`
    : "Live kudos, celebrations and reward momentum";
}

function renderRecognitionFeed() {
  const container = document.getElementById("recognition-feed");
  if (recognitionLoadError) {
    container.innerHTML = `<div class="empty-state">${escapeHtml(recognitionLoadError)}</div>`;
    return;
  }

  const posts = getFilteredRecognitionPosts();
  if (!appData.recognitionPosts.length) {
    container.innerHTML = `
      <div class="empty-state">
        No live recognition posts have been shared yet. The first kudos or milestone post will appear here.
      </div>
    `;
    return;
  }

  if (!posts.length) {
    const topicConfig = RECOGNITION_TOPIC_CONFIG[state.recognitionFilter];
    container.innerHTML = `
      <div class="empty-state">
        ${escapeHtml(topicConfig ? topicConfig.emptyCopy : "No recognition posts match this filter right now.")}
      </div>
    `;
    return;
  }

  container.innerHTML = posts.map(renderRecognitionPostCard).join("");
}

function renderRecognitionLeaderboardCard() {
  const container = document.getElementById("recognition-leaderboard-card");
  if (!container) {
    return;
  }

  container.innerHTML = `
    <p class="widget-kicker">Reward leaderboard</p>
    <h3>Who is earning the most points</h3>
    ${
      appData.leaderboard.length
        ? `<ul class="mini-list">
            ${appData.leaderboard.map((person) => `
              <li>
                <div>
                  <div class="mini-item-title">${escapeHtml(person.name)}</div>
                  <div class="mini-item-meta">${escapeHtml(person.title || "Employee")}</div>
                </div>
                <div class="mini-item-time">${escapeHtml(String(person.points))} pts</div>
              </li>
            `).join("")}
          </ul>`
        : `<div class="empty-state">Point rankings will appear once live recognition and reactions begin to build up.</div>`
    }
  `;
}

function renderRecognitionCelebrationsCard() {
  const container = document.getElementById("recognition-celebrations-card");
  if (!container) {
    return;
  }

  const birthdayItems = appData.birthdays.slice(0, 3).map((person) => `
    <li>
      <div>
        <div class="mini-item-title">${escapeHtml(person.name)}</div>
        <div class="mini-item-meta">${escapeHtml(person.title || "Birthday")}</div>
      </div>
      <div class="mini-item-time">${escapeHtml(person.date_label)}</div>
    </li>
  `).join("");
  const anniversaryItems = appData.anniversaries.slice(0, 3).map((person) => `
    <li>
      <div>
        <div class="mini-item-title">${escapeHtml(person.name)}</div>
        <div class="mini-item-meta">${escapeHtml(`${person.years} year${person.years === 1 ? "" : "s"}`)}</div>
      </div>
      <div class="mini-item-time">${escapeHtml(person.date_label)}</div>
    </li>
  `).join("");

  container.innerHTML = `
    <p class="widget-kicker">Celebrations</p>
    <h3>Birthdays and work anniversaries</h3>
    ${
      birthdayItems || anniversaryItems
        ? `<div class="celebration-stack">
            ${birthdayItems ? `<div><div class="mini-item-meta">Upcoming birthdays</div><ul class="mini-list">${birthdayItems}</ul></div>` : ""}
            ${anniversaryItems ? `<div><div class="mini-item-meta">Upcoming anniversaries</div><ul class="mini-list">${anniversaryItems}</ul></div>` : ""}
          </div>`
        : `<div class="empty-state">Employee celebrations will surface here from the live directory data.</div>`
    }
  `;
}

function renderRecognitionRewardsCard() {
  const container = document.getElementById("recognition-rewards-card");
  if (!container) {
    return;
  }

  container.innerHTML = `
    <p class="widget-kicker">My reward points</p>
    <h3>${escapeHtml(String(appData.currentUserPoints))} points</h3>
    <p>These points are now driven by live activity and can later become redeemable inside the Brand Store.</p>
    ${
      appData.rewardRules.length
        ? `<ul class="simple-list">
            ${appData.rewardRules.map((rule) => `
              <li>${escapeHtml(REWARD_RULE_LABELS[rule.key] || capitalize(rule.key.replaceAll("_", " ")))}: ${escapeHtml(String(rule.points))} pt${rule.points === 1 ? "" : "s"}</li>
            `).join("")}
          </ul>`
        : ""
    }
  `;
}

function renderStoreSummary() {
  const items = getFilteredStoreItems();
  const availableItems = appData.storeItems.filter((item) => item.available_units > 0).length;

  document.getElementById("store-summary-grid").innerHTML = [
    {
      kicker: "Balance",
      title: `${appData.storeBalance.available_points || 0} pts`,
      copy: "Available reward points that can be used on the current catalog.",
    },
    {
      kicker: "Catalog",
      title: `${appData.storeItems.length} live item${appData.storeItems.length === 1 ? "" : "s"}`,
      copy: "Admin-managed branded merchandise, memorabilia and desk items.",
    },
    {
      kicker: "Availability",
      title: `${availableItems} ready now`,
      copy: "Items with at least one available unit for redemption.",
    },
    {
      kicker: "My requests",
      title: `${appData.storeRedemptions.length} request${appData.storeRedemptions.length === 1 ? "" : "s"}`,
      copy: items.length
        ? `${items.length} items match the current filter.`
        : "Switch category filters to browse more of the store catalog.",
    },
  ].map((item) => `
    <article class="mini-panel">
      <p class="widget-kicker">${escapeHtml(item.kicker)}</p>
      <h3>${escapeHtml(item.title)}</h3>
      <p class="muted-copy">${escapeHtml(item.copy)}</p>
    </article>
  `).join("");
}

function renderStoreCatalog() {
  const container = document.getElementById("store-catalog-grid");
  if (storeLoadError) {
    document.getElementById("store-results-meta").textContent = "Store load issue";
    container.innerHTML = `<div class="empty-state">${escapeHtml(storeLoadError)}</div>`;
    return;
  }

  const items = getFilteredStoreItems();
  document.getElementById("store-results-meta").textContent = appData.storeItems.length
    ? `${items.length} of ${appData.storeItems.length} brand-store items shown`
    : "Live Acuité brand-store catalog";

  if (!appData.storeItems.length) {
    container.innerHTML = `
      <div class="empty-state">
        The Brand Store catalog is empty right now. Once admins upload merchandise in the backend, employees will be able to redeem it here.
      </div>
    `;
    return;
  }

  if (!items.length) {
    container.innerHTML = `
      <div class="empty-state">
        No store items match that category right now. Try a broader filter.
      </div>
    `;
    return;
  }

  container.innerHTML = items.map(renderStoreItemCard).join("");
}

function renderStoreBalanceCard() {
  document.getElementById("store-balance-card").innerHTML = `
    <p class="widget-kicker">My points</p>
    <h3>${escapeHtml(String(appData.storeBalance.available_points || 0))} available</h3>
    <ul class="simple-list">
      <li>Earned: ${escapeHtml(String(appData.storeBalance.earned_points || 0))} pts</li>
      <li>Locked in redemptions: ${escapeHtml(String(appData.storeBalance.locked_points || 0))} pts</li>
      <li>Use Recognition &amp; Rewards to keep building your balance.</li>
    </ul>
  `;
}

function renderStoreRedemptionsCard() {
  document.getElementById("store-redemptions-card").innerHTML = `
    <p class="widget-kicker">My redemptions</p>
    <h3>Recent requests</h3>
    ${
      appData.storeRedemptions.length
        ? `<ul class="mini-list">
            ${appData.storeRedemptions.map((item) => `
              <li>
                <div>
                  <div class="mini-item-title">${escapeHtml(item.item.name)}</div>
                  <div class="mini-item-meta">${escapeHtml(item.item.category_label)}</div>
                </div>
                <div class="learning-req-status ${escapeHtml(item.status)}">${escapeHtml(capitalize(item.status))}</div>
              </li>
            `).join("")}
          </ul>`
        : `<div class="empty-state">Your brand-store requests will appear here after your first redemption.</div>`
    }
  `;
}

function renderStorePolicyCard() {
  document.getElementById("store-policy-card").innerHTML = `
    <p class="widget-kicker">How it works</p>
    <h3>Redemption rules</h3>
    <ul class="simple-list">
      <li>Items are redeemed using available Connect reward points.</li>
      <li>Submitting a request locks points until the request is fulfilled, declined or cancelled.</li>
      <li>Stock visibility is live, so employees only request items that are still available.</li>
    </ul>
  `;
}

function renderStoreItemCard(item) {
  const accent = item.accent_hex || "#e8722a";
  const activeRedemption = appData.storeRedemptions.find((redemption) => {
    return redemption.item.id === item.id
      && ["requested", "approved", "fulfilled"].includes(redemption.status);
  });
  const availablePoints = Number(appData.storeBalance.available_points || 0);
  const missingPoints = Math.max(item.point_cost - availablePoints, 0);
  const outOfStock = item.available_units <= 0;
  const canRedeem = !activeRedemption && !outOfStock && availablePoints >= item.point_cost;
  let actionLabel = "Redeem";

  if (activeRedemption) {
    actionLabel = capitalize(activeRedemption.status);
  } else if (outOfStock) {
    actionLabel = "Out of stock";
  } else if (missingPoints > 0) {
    actionLabel = `Need ${missingPoints} pts`;
  }

  return `
    <article class="tool-card store-item-card" id="store-item-${item.id}">
      <div class="store-item-art" style="background:${escapeHtml(accent)}">
        <span>${escapeHtml(STORE_CATEGORY_LABELS[item.category] || item.category_label || "Store")}</span>
      </div>
      <div class="store-item-copy">
        <div class="tool-card-head store-item-head">
          <div>
            <h3>${escapeHtml(item.name)}</h3>
            <span class="tool-status ${item.available_units > 0 ? "live" : "planned"}">${escapeHtml(item.category_label)}</span>
          </div>
          <div class="store-item-cost">${escapeHtml(String(item.point_cost))} pts</div>
        </div>
        <p>${escapeHtml(item.description || "Admin-managed branded merchandise available for point redemption inside Connect.")}</p>
        <div class="store-item-meta">
          <span class="mini-chip ${item.available_units > 0 ? "success" : ""}">
            ${escapeHtml(`${item.available_units} available`)}
          </span>
          <span class="mini-item-meta">${escapeHtml(`${item.stock_units} total stock`)}</span>
        </div>
      </div>
      <div class="tool-meta store-item-footer">
        <span class="mini-item-meta">
          ${activeRedemption
            ? escapeHtml(`You already have a ${activeRedemption.status.replaceAll("_", " ")} request`)
            : escapeHtml(`Use ${item.point_cost} points to request this item`)}
        </span>
        <button
          type="button"
          class="tool-open ${canRedeem ? "live" : ""}"
          data-action="redeem-store-item"
          data-id="${item.id}"
          ${canRedeem ? "" : "disabled"}
        >
          ${escapeHtml(actionLabel)}
        </button>
      </div>
    </article>
  `;
}

function renderBulletinPanel() {
  const container = document.getElementById("bulletin-feed");
  const meta = document.getElementById("bulletin-results-meta");
  if (!container || !meta) {
    return;
  }

  if (bulletinLoadError) {
    meta.textContent = "Bulletin services issue";
    container.innerHTML = `<div class="empty-state">${escapeHtml(bulletinLoadError)}</div>`;
    return;
  }

  const posts = getFilteredBulletinPosts();
  meta.textContent = appData.bulletinPosts.length
    ? `${posts.length} of ${appData.bulletinPosts.length} bulletin posts shown`
    : "Live company announcement board";

  if (!appData.bulletinPosts.length) {
    container.innerHTML = `
      <div class="empty-state">
        No company bulletin posts have been published yet. The first town hall, advisory or event note will appear here.
      </div>
    `;
    return;
  }

  if (!posts.length) {
    container.innerHTML = `<div class="empty-state">No bulletin posts match this filter right now.</div>`;
    return;
  }

  container.innerHTML = posts.map(renderBulletinPostCard).join("");
}

function renderAdminPanel() {
  const panel = document.getElementById("panel-admin");
  if (!panel) {
    return;
  }
  if (!currentUserCanAdministerConnect()) {
    panel.hidden = true;
    return;
  }

  panel.hidden = false;
  renderAdminUserList();
  renderAdminEditForm();
  renderAdminBulletinTemplates();
  if (elements.adminBulletinForm && !elements.adminBulletinForm.elements.title.value && !elements.adminBulletinForm.elements.body.value) {
    applyBulletinTemplate(selectedBulletinTemplateKey);
  }
}

function renderAdminUserList() {
  if (!elements.adminUserList || !elements.adminUserResultsMeta) {
    return;
  }
  if (adminUsersLoadError) {
    elements.adminUserResultsMeta.textContent = "Admin data issue";
    elements.adminUserList.innerHTML = `<div class="empty-state">${escapeHtml(adminUsersLoadError)}</div>`;
    return;
  }

  const query = String(elements.adminUserSearchInput?.value || "").trim().toLowerCase();
  const users = appData.adminUsers.filter((user) => {
    if (!query) {
      return true;
    }
    return [
      user.name,
      user.email,
      user.title,
      user.department,
      user.location,
      user.employee_code,
      user.access_level,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase()
      .includes(query);
  });

  elements.adminUserResultsMeta.textContent = appData.adminUsers.length
    ? `${users.length} of ${appData.adminUsers.length} employees shown`
    : "No employee accounts loaded yet";

  if (!users.length) {
    elements.adminUserList.innerHTML = `<div class="empty-state">No employee matches that search.</div>`;
    return;
  }

  elements.adminUserList.innerHTML = users.slice(0, 30).map((user) => `
    <button
      type="button"
      class="admin-user-card ${selectedAdminUserId === user.id ? "active" : ""}"
      data-action="select-admin-user"
      data-id="${user.id}"
    >
      <div>
        <div class="mini-item-title">${escapeHtml(user.name || user.email)}</div>
        <div class="mini-item-meta">${escapeHtml([user.title, user.location].filter(Boolean).join(" | ") || user.email)}</div>
      </div>
      <div class="admin-user-badges">
        <span class="mini-chip">${escapeHtml(capitalize(user.access_level || "employee"))}</span>
        <span class="mini-chip ${user.can_post_in_connect ? "success" : ""}">${escapeHtml(user.can_post_in_connect ? "Posting on" : "Posting off")}</span>
      </div>
    </button>
  `).join("");
}

function renderAdminEditForm() {
  if (!elements.adminEditUserForm) {
    return;
  }
  const user = appData.adminUsers.find((item) => item.id === selectedAdminUserId);
  const controls = elements.adminEditUserForm.querySelectorAll("input, select, button");

  if (!user) {
    elements.adminEditUserForm.reset();
    if (elements.adminEditStatus) {
      elements.adminEditStatus.textContent = "Select an employee to edit their account.";
    }
    controls.forEach((control) => {
      if (control.type !== "hidden") {
        control.disabled = true;
      }
    });
    if (elements.adminEditSubmit) {
      elements.adminEditSubmit.disabled = true;
    }
    return;
  }

  if (elements.adminEditUserId) elements.adminEditUserId.value = String(user.id);
  if (elements.adminEditDisplayName) elements.adminEditDisplayName.value = user.name || "";
  if (elements.adminEditEmail) elements.adminEditEmail.value = user.email || "";
  if (elements.adminEditTitle) elements.adminEditTitle.value = user.title || "";
  if (elements.adminEditDepartment) elements.adminEditDepartment.value = user.department || "";
  if (elements.adminEditLocation) elements.adminEditLocation.value = user.location || "";
  if (elements.adminEditCode) elements.adminEditCode.value = user.employee_code || "";
  if (elements.adminEditAccessLevel) elements.adminEditAccessLevel.value = user.access_level || "employee";
  if (elements.adminEditEmploymentStatus) elements.adminEditEmploymentStatus.value = user.employment_status || "active";
  if (elements.adminEditCanPost) elements.adminEditCanPost.checked = Boolean(user.can_post_in_connect);
  if (elements.adminEditIsActive) elements.adminEditIsActive.checked = Boolean(user.is_active);
  if (elements.adminEditStatus) {
    elements.adminEditStatus.textContent = `Editing ${user.name || user.email}. Save to update access, posting and account status.`;
  }
  controls.forEach((control) => {
    if (control.type !== "hidden") {
      control.disabled = false;
    }
  });
}

function renderAdminBulletinTemplates() {
  if (!elements.adminBulletinTemplates) {
    return;
  }
  elements.adminBulletinTemplates.innerHTML = BULLETIN_TEMPLATE_LIBRARY.map((template) => `
    <button
      type="button"
      class="admin-template-chip ${selectedBulletinTemplateKey === template.key ? "active" : ""}"
      data-action="apply-bulletin-template"
      data-template-key="${template.key}"
    >
      ${escapeHtml(template.label)}
    </button>
  `).join("");
}

function applyBulletinTemplate(templateKey) {
  const template = BULLETIN_TEMPLATE_LIBRARY.find((item) => item.key === templateKey);
  if (!template || !elements.adminBulletinForm) {
    return;
  }
  selectedBulletinTemplateKey = template.key;
  elements.adminBulletinForm.elements.category.value = template.category;
  elements.adminBulletinForm.elements.title.value = template.title;
  elements.adminBulletinForm.elements.body.value = template.body;
  renderAdminBulletinTemplates();
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
    if (selectedDepartments.length && !selectedDepartments.includes(person.departmentForConnect)) {
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
          ${renderDirectoryAvatar(person)}
          <div class="person-meta">
            <h3>${escapeHtml(person.name)}</h3>
            <div class="person-role">${escapeHtml(person.role)}</div>
            <div class="person-location">${escapeHtml(person.officeLine)}</div>
          </div>
        </div>
        <div class="person-detail-grid">
          ${directoryCardDetail("Employee Code", person.employeeCode)}
          ${directoryCardDetail("Company", person.companyLabel || person.company)}
          ${directoryCardDetail("Office", person.office)}
          ${directoryCardDetail("Joined", person.joinedOn)}
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
      <div class="bday-avatar" style="background:${gradientValue(person.gradient || gradientKeyFromText(person.name))}">${escapeHtml(person.initials)}</div>
      <div class="bday-info">
        <div class="name">${escapeHtml(person.name)}</div>
        <div class="date ${person.highlight ? "today" : ""}">${escapeHtml(person.date_label || person.date)}</div>
      </div>
    </div>
  `).join("") : `<div class="empty-state">Birthday highlights will appear once live employee celebrations are configured.</div>`;
}

function renderAnniversaries() {
  document.getElementById("anniversaries-list").innerHTML = appData.anniversaries.length ? appData.anniversaries.map((person) => `
    <div class="bday-item">
      <div class="bday-avatar" style="background:${gradientValue(person.gradient || gradientKeyFromText(person.name))}">${escapeHtml(person.initials)}</div>
      <div class="bday-info">
        <div class="name">${escapeHtml(person.name)}</div>
        <div class="date ${person.highlight ? "today" : ""}">${escapeHtml(person.date_label || person.date)}${person.years ? ` - ${escapeHtml(String(person.years))} yr${person.years === 1 ? "" : "s"}` : ""}</div>
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
        <button
          type="button"
          class="action-btn ${post.currentUserHasReacted ? "liked" : ""}"
          data-action="toggle-live-reaction"
          data-id="${post.sourceId}"
        >
          ${likeIcon()}${escapeHtml(String(post.reactionCount))}
        </button>
        <button type="button" class="action-btn" data-action="open-live-comments" data-id="${post.sourceId}">
          ${commentIcon()}${escapeHtml(String(post.commentCount))}
        </button>
        <div class="spacer"></div>
        ${renderDeleteLivePostButton(post, "community")}
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
  if (!currentUserCanCreatePosts()) {
    showToast("Your posting access is currently disabled.");
    return;
  }
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

async function redeemStoreItem(itemId) {
  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/store/redemptions/", {
      method: "POST",
      body: {
        item_id: Number(itemId),
      },
    });

    if (payload.redemption) {
      await loadStoreData();
      renderStorePanel();
      renderRecognitionRewardsCard();
      showToast(`Redemption request placed for ${payload.redemption.item.name}.`);
      return;
    }

    showToast("Store redemption submitted.");
  } catch (error) {
    showToast(error.message || "Could not place the redemption request.");
  }
}

async function submitAdminCreateUser() {
  if (!currentUserCanAdministerConnect()) {
    showToast("Admin access is required for account creation.");
    return;
  }
  const formData = new FormData(elements.adminCreateUserForm);
  const displayName = String(formData.get("display_name") || "").trim();
  const email = String(formData.get("email") || "").trim();

  if (!displayName || !email) {
    showToast("Add at least employee name and email.");
    return;
  }

  try {
    await window.AcuiteConnectAuth.apiRequest("/api/accounts/access/users/", {
      method: "POST",
      body: {
        display_name: displayName,
        email,
        title: String(formData.get("title") || "").trim(),
        department: String(formData.get("department") || "").trim(),
        location: String(formData.get("location") || "").trim(),
        employee_code: String(formData.get("employee_code") || "").trim(),
        access_level: String(formData.get("access_level") || "employee"),
        can_post_in_connect: formData.get("can_post_in_connect") === "on",
      },
    });
    elements.adminCreateUserForm.reset();
    await Promise.all([loadAdminUsers(), loadDirectoryData()]);
    renderAdminPanel();
    renderDirectory();
    showToast(`Account created for ${email}.`);
  } catch (error) {
    showToast(error.message || "Could not create the employee account.");
  }
}

async function submitAdminEditUser() {
  if (!currentUserCanAdministerConnect()) {
    showToast("Admin access is required to edit accounts.");
    return;
  }
  const userId = Number(elements.adminEditUserId?.value || 0);
  if (!userId) {
    showToast("Select an employee to edit first.");
    return;
  }

  const formData = new FormData(elements.adminEditUserForm);
  try {
    await window.AcuiteConnectAuth.apiRequest(`/api/accounts/access/users/${userId}/`, {
      method: "PATCH",
      body: {
        display_name: String(formData.get("display_name") || "").trim(),
        title: String(formData.get("title") || "").trim(),
        department: String(formData.get("department") || "").trim(),
        location: String(formData.get("location") || "").trim(),
        employee_code: String(formData.get("employee_code") || "").trim(),
        access_level: String(formData.get("access_level") || "employee"),
        employment_status: String(formData.get("employment_status") || "active"),
        can_post_in_connect: formData.get("can_post_in_connect") === "on",
        is_active: formData.get("is_active") === "on",
      },
    });
    await Promise.all([loadAdminUsers(), loadDirectoryData()]);
    renderAdminPanel();
    renderDirectory();
    showToast("Employee account updated.");
  } catch (error) {
    showToast(error.message || "Could not update the employee account.");
  }
}

async function submitAdminBulletinPost() {
  if (!currentUserCanAdministerConnect()) {
    showToast("Admin access is required to publish bulletin posts.");
    return;
  }

  const formData = new FormData(elements.adminBulletinForm);
  const title = String(formData.get("title") || "").trim();
  const body = String(formData.get("body") || "").trim();
  const category = String(formData.get("category") || "announcements").trim().toLowerCase();

  if (!title || !body) {
    showToast("Add both a headline and message before publishing.");
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
      method: "POST",
      body: {
        title,
        body,
        kind: "announcement",
        module: "general",
        topic: category,
        post_as_company: true,
        allow_comments: formData.get("allow_comments") === "on",
        pinned: formData.get("pinned") === "on",
        metadata: {
          bulletin_category: category,
          bulletin_template: selectedBulletinTemplateKey,
        },
      },
    });
    showToast(
      payload.post && formData.get("pinned") === "on"
        ? "Pinned company bulletin published."
        : "Company bulletin published."
    );
    await loadBulletinPosts();
    renderBulletinPanel();
    switchTab("bulletin");
  } catch (error) {
    showToast(error.message || "Could not publish the bulletin post.");
  }
}

async function deleteLivePost(postId, moduleName) {
  if (!postId) {
    return;
  }
  const confirmed = window.confirm("Delete this post?");
  if (!confirmed) {
    return;
  }
  try {
    await window.AcuiteConnectAuth.apiRequest(`/api/feed/posts/${postId}/`, {
      method: "DELETE",
    });
    await Promise.all([
      loadCommunityPosts(),
      loadVoiceData(),
      loadRecognitionData(),
      loadBulletinPosts(),
    ]);
    renderAll();
    showToast(moduleName === "general" ? "Bulletin post deleted." : "Post deleted.");
  } catch (error) {
    showToast(error.message || "Could not delete the post.");
  }
}

function submitKudos() {
  if (!currentUserCanCreatePosts()) {
    showToast("Your posting access is currently disabled.");
    return;
  }
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
  if (!currentUserCanCreatePosts()) {
    showToast("Your posting access is currently disabled.");
    return;
  }
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

  const recognition = appData.recognitionPosts.map((post) => ({
    title: post.title,
    subtitle: `${post.topicLabel} - ${post.recipientName || post.authorName}`,
    type: "recognition",
    tab: "recognition",
    targetId: post.id,
    searchText: [
      post.title,
      post.body,
      post.topicLabel,
      post.recipientName,
      post.tagLabel,
      post.authorName,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase(),
  }));

  const bulletin = appData.bulletinPosts.map((post) => ({
    title: post.title,
    subtitle: `${post.authorName} - Bulletin`,
    type: "post",
    tab: "bulletin",
    targetId: post.id,
    searchText: [post.title, post.authorName, post.body.join(" "), post.categoryLabel].join(" ").toLowerCase(),
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
  const store = appData.storeItems.map((item) => ({
    title: item.name,
    subtitle: `${item.category_label} - ${item.point_cost} pts`,
    type: "store",
    tab: "store",
    targetId: `store-item-${item.id}`,
    searchText: [
      item.name,
      item.category_label,
      item.description,
      item.point_cost,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase(),
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

  return [...community, ...voice, ...recognition, ...bulletin, ...directory, ...tools, ...resources, ...books, ...store, ...poll];
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

  if (group === "recognition") {
    state.recognitionFilter = value;
    saveState();
    renderRecognitionPanel();
    syncFilterButtons();
    return;
  }

  if (group === "store") {
    state.storeFilter = value;
    saveState();
    renderStorePanel();
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
    recognition: state.recognitionFilter,
    store: state.storeFilter,
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
    allowComments: Boolean(post.allow_comments),
    commentCount: post.comment_count || 0,
    authorName: author.name || "Acuité employee",
    authorMeta: [author.title, author.location].filter(Boolean).join(" | ") || author.email || "Employee",
    initials: author.initials || initialsFromName(author.name || "Acuité"),
    avatar: gradientKeyFromText(`${author.name || ""}-${board}-${communityType}`),
    postedAtLabel: formatRelativeTime(post.published_at || post.created_at),
    createdAt: post.created_at || "",
    reactionCount: post.reaction_count || 0,
    currentUserHasReacted: Boolean(post.current_user_has_reacted),
    canDelete: Boolean(post.viewer_can_delete),
    isAuthor: Boolean(post.viewer_is_author),
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
    allowComments: Boolean(post.allow_comments),
    commentCount: post.comment_count || 0,
    authorName,
    authorMeta: [author.title, author.location].filter(Boolean).join(" | ") || author.email || "Employee",
    initials: author.initials || initialsFromName(authorName),
    avatar: gradientKeyFromText(`${authorName}-${topic}`),
    postedAtLabel: formatRelativeTime(post.published_at || post.created_at),
    createdAt: post.created_at || "",
    pinned: Boolean(post.pinned),
    reactionCount: post.reaction_count || 0,
    currentUserHasReacted: Boolean(post.current_user_has_reacted),
    canDelete: Boolean(post.viewer_can_delete),
    isAuthor: Boolean(post.viewer_is_author),
  };
}

function mapRecognitionPost(post) {
  const topic = post.topic || "kudos";
  const topicConfig = RECOGNITION_TOPIC_CONFIG[topic] || RECOGNITION_TOPIC_CONFIG.kudos;
  const metadata = post.metadata || {};
  const author = post.author || {};
  const authorName = author.name || "Acuité employee";

  return {
    id: `recognition-post-${post.id}`,
    sourceId: post.id,
    title: post.title,
    body: post.body,
    topic,
    topicLabel: topicConfig.label,
    topicKicker: topicConfig.kicker,
    tag: metadata.recognition_tag || "",
    tagLabel: getRecognitionTagLabel(topic, metadata.recognition_tag || ""),
    recipientUserId: metadata.recipient_user_id || null,
    recipientName: metadata.recipient_name || "",
    recipientInitials: metadata.recipient_initials || initialsFromName(metadata.recipient_name || "Acuité"),
    authorName,
    authorMeta: [author.title, author.location].filter(Boolean).join(" | ") || author.email || "Employee",
    initials: author.initials || initialsFromName(authorName),
    avatar: gradientKeyFromText(`${authorName}-${topic}-${metadata.recipient_name || ""}`),
    postedAtLabel: formatRelativeTime(post.published_at || post.created_at),
    createdAt: post.created_at || "",
    allowComments: Boolean(post.allow_comments),
    commentCount: post.comment_count || 0,
    reactionCount: post.reaction_count || 0,
    currentUserHasReacted: Boolean(post.current_user_has_reacted),
    canDelete: Boolean(post.viewer_can_delete),
    isAuthor: Boolean(post.viewer_is_author),
  };
}

function mapBulletinPost(post) {
  const metadata = post.metadata || {};
  const author = post.author || {};
  const category = (post.topic || metadata.bulletin_category || "announcements").toLowerCase();
  const authorName = author.name || "Acuité Ratings & Research";

  return {
    id: `bulletin-post-${post.id}`,
    sourceId: post.id,
    title: post.title,
    body: Array.isArray(post.body) ? post.body : [post.body],
    category,
    categoryLabel: BULLETIN_CATEGORY_LABELS[category] || capitalize(category),
    templateKey: metadata.bulletin_template || "",
    metaLines: Array.isArray(metadata.bulletin_meta_lines)
      ? metadata.bulletin_meta_lines.filter((line) => typeof line === "string" && line.trim())
      : [],
    ctaLabel: String(metadata.bulletin_cta_label || "").trim(),
    ctaTarget: String(metadata.bulletin_cta_target || "").trim(),
    imageDataUrl: String(metadata.bulletin_image_data_url || "").trim(),
    imageAlt: String(metadata.bulletin_image_alt || post.title || "Bulletin image").trim(),
    bulletinCard: metadata.bulletin_card && typeof metadata.bulletin_card === "object" ? metadata.bulletin_card : null,
    authorName,
    authorMeta: [author.title, author.location].filter(Boolean).join(" | ") || "Company bulletin",
    initials: author.initials || initialsFromName(authorName),
    avatar: gradientKeyFromText(`${authorName}-${category}`),
    postedAtLabel: formatRelativeTime(post.published_at || post.created_at),
    createdAt: post.created_at || "",
    allowComments: Boolean(post.allow_comments),
    commentCount: post.comment_count || 0,
    reactionCount: post.reaction_count || 0,
    currentUserHasReacted: Boolean(post.current_user_has_reacted),
    canDelete: Boolean(post.viewer_can_delete),
    isAuthor: Boolean(post.viewer_is_author),
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

function getFilteredBulletinPosts() {
  const posts = appData.bulletinPosts.slice().sort((left, right) => {
    return new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime();
  });
  if (state.bulletinFilter === "all") {
    return posts;
  }
  return posts.filter((post) => post.category === state.bulletinFilter);
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

function getFilteredRecognitionPosts() {
  const posts = appData.recognitionPosts.slice().sort((left, right) => {
    return new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime();
  });
  if (state.recognitionFilter === "all") {
    return posts;
  }
  return posts.filter((post) => post.topic === state.recognitionFilter);
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

function getFilteredStoreItems() {
  if (state.storeFilter === "all") {
    return appData.storeItems.slice();
  }
  return appData.storeItems.filter((item) => item.category === state.storeFilter);
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

  const options = currentUserCanAdministerConnect()
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

function syncRecognitionComposer() {
  if (!elements.recognitionTopicSelect || !elements.recognitionTagSelect || !elements.recognitionTagLabel || !elements.recognitionRecipientSelect) {
    return;
  }

  const topic = elements.recognitionTopicSelect.value || "kudos";
  const config = RECOGNITION_TOPIC_CONFIG[topic] || RECOGNITION_TOPIC_CONFIG.kudos;
  const previousTag = elements.recognitionTagSelect.value;
  const previousRecipient = elements.recognitionRecipientSelect.value;

  elements.recognitionTagLabel.textContent = config.tagLabel;
  elements.recognitionTagSelect.innerHTML = config.tags.map((tag) => `
    <option value="${escapeHtml(tag.value)}">${escapeHtml(tag.label)}</option>
  `).join("");

  if (config.tags.some((tag) => tag.value === previousTag)) {
    elements.recognitionTagSelect.value = previousTag;
  }

  elements.recognitionRecipientSelect.innerHTML = `
    <option value="">Select employee</option>
    ${appData.directory.map((person) => `
      <option value="${escapeHtml(String(person.sourceUserId || ""))}">${escapeHtml(`${person.name} - ${person.role}`)}</option>
    `).join("")}
  `;

  if (appData.directory.some((person) => String(person.sourceUserId) === previousRecipient)) {
    elements.recognitionRecipientSelect.value = previousRecipient;
  }
}

async function submitVoicePost() {
  if (!currentUserCanCreatePosts()) {
    showToast("Your posting access is currently disabled.");
    return;
  }
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

async function submitRecognitionPost() {
  if (!currentUserCanCreatePosts()) {
    showToast("Your posting access is currently disabled.");
    return;
  }
  const formData = new FormData(elements.recognitionForm);
  const topic = String(formData.get("topic") || "").trim();
  const tag = String(formData.get("tag") || "").trim();
  const recipientUserId = Number(formData.get("recipient_user_id") || 0);
  const title = String(formData.get("title") || "").trim();
  const body = String(formData.get("body") || "").trim();
  const recipient = appData.directory.find((person) => person.sourceUserId === recipientUserId);

  if (!topic || !tag || !recipientUserId || !title || !body || !recipient) {
    showToast("Choose the type, tag, recipient, title and note before posting recognition.");
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
      method: "POST",
      body: {
        title,
        body,
        module: "recognition",
        topic,
        metadata: {
          recognition_tag: tag,
          recipient_user_id: recipient.sourceUserId,
          recipient_name: recipient.name,
          recipient_initials: recipient.initials,
        },
      },
    });

    if (payload.post) {
      appData.recognitionPosts.unshift(mapRecognitionPost(payload.post));
      await loadRecognitionData();
      elements.recognitionForm.reset();
      syncRecognitionComposer();
      renderRecognitionPanel();
      renderBirthdays();
      renderAnniversaries();
      showToast("Recognition shared live inside Connect.");
      return;
    }

    showToast("Recognition post created.");
  } catch (error) {
    showToast(error.message || "Could not post recognition.");
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

async function toggleLiveReaction(postId) {
  if (!postId) {
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest(`/api/feed/posts/${postId}/reactions/toggle/`, {
      method: "POST",
    });
    if (payload.post) {
      updateLivePostFromPayload(payload.post);
      await loadRecognitionData();
      renderCommunityPanel();
      renderVoicePanel();
      renderRecognitionPanel();
      renderBirthdays();
      renderAnniversaries();
      showToast(payload.reacted ? "Appreciation recorded." : "Appreciation removed.");
      return;
    }

    showToast("Reaction updated.");
  } catch (error) {
    showToast(error.message || "Could not update appreciation.");
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
    recognitionFilter: (
      typeof saved.recognitionFilter === "string"
      && ["all", ...Object.keys(RECOGNITION_TOPIC_CONFIG)].includes(saved.recognitionFilter)
    )
      ? saved.recognitionFilter
      : defaultState.recognitionFilter,
    storeFilter: (
      typeof saved.storeFilter === "string"
      && ["all", ...Object.keys(STORE_CATEGORY_LABELS)].includes(saved.storeFilter)
    )
      ? saved.storeFilter
      : defaultState.storeFilter,
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
    homeAnnouncementLiked: Boolean(saved.homeAnnouncementLiked),
    homeAnnouncementInterested: Boolean(saved.homeAnnouncementInterested),
    homeAnnouncementBooked: Boolean(saved.homeAnnouncementBooked),
    homeAnnouncementCalendarBlocked: Boolean(saved.homeAnnouncementCalendarBlocked),
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

function downloadAnnouncementCalendarInvite() {
  const calendar = FEATURED_HOME_ANNOUNCEMENT.calendar;
  const content = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Acuite Connect//EN",
    "BEGIN:VEVENT",
    `UID:${FEATURED_HOME_ANNOUNCEMENT.id}@connect.acuite-group.com`,
    `DTSTAMP:${toICSDateTime(new Date().toISOString())}`,
    `DTSTART:${toICSDateTime(calendar.start)}`,
    `DTEND:${toICSDateTime(calendar.end)}`,
    `SUMMARY:${escapeICS(calendar.title)}`,
    `DESCRIPTION:${escapeICS(calendar.description)}`,
    `LOCATION:${escapeICS(calendar.location)}`,
    "END:VEVENT",
    "END:VCALENDAR",
  ].join("\r\n");

  const blob = new Blob([content], { type: "text/calendar;charset=utf-8" });
  const objectUrl = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = objectUrl;
  link.download = "acuite-connect-town-hall.ics";
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => {
    window.URL.revokeObjectURL(objectUrl);
  }, 1000);
}

function toICSDateTime(value) {
  const date = value instanceof Date ? value : new Date(value);
  return date.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z");
}

function escapeICS(value) {
  return String(value)
    .replaceAll("\\", "\\\\")
    .replaceAll("\n", "\\n")
    .replaceAll(",", "\\,")
    .replaceAll(";", "\\;");
}

function createDirectoryFilterOptions() {
  return {
    company: [],
    location: [],
    department: [],
  };
}

function createProfileBuilderDraft() {
  return {
    skills: [],
    hobbiesText: "",
    interestsText: "",
    photos: [],
  };
}

function createProfileDraftFromProfile(profile) {
  if (!profile) {
    return createProfileBuilderDraft();
  }
  return {
    skills: Array.isArray(profile.skills) ? profile.skills.slice(0, 10) : [],
    hobbiesText: Array.isArray(profile.hobbies) ? profile.hobbies.join(", ") : "",
    interestsText: Array.isArray(profile.interests) ? profile.interests.join(", ") : "",
    photos: Array.isArray(profile.profile_photos) ? profile.profile_photos.slice(0, 2) : [],
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

function getRecognitionTopicLabel(topic) {
  return (RECOGNITION_TOPIC_CONFIG[topic] && RECOGNITION_TOPIC_CONFIG[topic].label)
    || capitalize(String(topic || "").replaceAll("_", " "));
}

function getRecognitionTagLabel(topic, tag) {
  const config = RECOGNITION_TOPIC_CONFIG[topic];
  const match = config ? config.tags.find((item) => item.value === tag) : null;
  return match ? match.label : capitalize(String(tag || "").replaceAll("_", " "));
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

function renderDirectoryAvatar(person) {
  const primaryPhoto = person.profilePhotos[0] || "";
  if (primaryPhoto) {
    return `
      <div class="person-avatar has-photo" style="background-image:url('${escapeHtml(primaryPhoto)}')">
        ${escapeHtml(person.initials)}
      </div>
    `;
  }
  return `<div class="person-avatar" style="background:${gradientValue(person.gradient)}">${escapeHtml(person.initials)}</div>`;
}

function setAvatarElement(element, { initials, gradient, photoUrl }) {
  if (!element) {
    return;
  }

  element.classList.toggle("has-photo", Boolean(photoUrl));
  element.style.background = photoUrl ? "" : gradientValue(gradient);
  element.style.backgroundImage = photoUrl ? `url("${photoUrl}")` : "";
  element.style.backgroundSize = photoUrl ? "cover" : "";
  element.style.backgroundPosition = photoUrl ? "center" : "";
  element.textContent = photoUrl ? initials : initials;
}

function toggleProfileMenu() {
  profileMenuOpen = !profileMenuOpen;
  renderProfile();
}

function closeProfileMenu() {
  if (!profileMenuOpen) {
    return;
  }
  profileMenuOpen = false;
  renderProfile();
}

function openProfileBuilder() {
  if (!elements.profileModalBackdrop) {
    return;
  }
  elements.profileModalBackdrop.hidden = false;
  document.body.classList.add("modal-open");
}

function closeProfileBuilder() {
  if (!elements.profileModalBackdrop) {
    return;
  }
  elements.profileModalBackdrop.hidden = true;
  document.body.classList.remove("modal-open");
}

function mapDirectoryProfileToCard(profile) {
  const company = profile.company_name || "";
  const companyLabel = displayCompanyName(company);
  const department = profile.department || "";
  const departmentForConnect = profile.department_for_connect || "";
  const functionName = profile.function_name || "";
  const office = profile.office_location || profile.location || profile.city || "";
  const joinedOn = formatDisplayDate(profile.joined_on);
  const contactLine = [profile.email, profile.mobile_number || profile.phone_number].filter(Boolean).join(" | ");
  const skills = Array.isArray(profile.skills) ? profile.skills : [];
  const hobbies = Array.isArray(profile.hobbies) ? profile.hobbies : [];
  const interests = Array.isArray(profile.interests) ? profile.interests : [];
  const profilePhotos = Array.isArray(profile.profile_photos) ? profile.profile_photos.slice(0, 2) : [];
  const teams = [companyLabel, department, functionName].filter(Boolean);

  return {
    id: `person-${profile.id}`,
    sourceUserId: profile.id,
    name: profile.name,
    initials: profile.initials || initialsFromName(profile.name),
    role: profile.title || "Employee",
    city: profile.city || office,
    company,
    companyLabel,
    department,
    departmentForConnect,
    functionName,
    office,
    officeLine: [office, companyLabel].filter(Boolean).join(" | "),
    employeeCode: profile.employee_code || "",
    joinedOn,
    contactLine,
    teams,
    skills,
    hobbies,
    interests,
    profilePhotos,
    blurb: profile.bio || profile.expertise || "",
    searchText: [
      profile.name,
      profile.email,
      profile.title,
      company,
      companyLabel,
      department,
      departmentForConnect,
      functionName,
      office,
      profile.location,
      profile.mobile_number,
      profile.employee_code,
      ...skills,
      ...hobbies,
      ...interests,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase(),
    gradient: gradientKeyFromText(`${company}-${department}-${profile.name}`),
  };
}

function toggleProfileSkill(skill) {
  if (!skill) {
    return;
  }
  if (profileBuilderDraft.skills.includes(skill)) {
    profileBuilderDraft.skills = profileBuilderDraft.skills.filter((item) => item !== skill);
    renderProfileBuilder();
    return;
  }
  if (profileBuilderDraft.skills.length >= 10) {
    showToast("You can select up to 10 skills.");
    return;
  }
  profileBuilderDraft.skills = [...profileBuilderDraft.skills, skill];
  renderProfileBuilder();
}

function clearProfilePhoto(index) {
  if (Number.isNaN(index) || index < 0 || index > 1) {
    return;
  }
  profileBuilderDraft.photos[index] = "";
  renderProfileBuilder();
}

async function handleProfilePhotoSelection(event, index) {
  const file = event.target.files && event.target.files[0];
  if (!file) {
    return;
  }
  if (!file.type.startsWith("image/")) {
    showToast("Choose an image file for the profile photo.");
    event.target.value = "";
    return;
  }
  if (file.size > 1_500_000) {
    showToast("Each profile photo should be under 1.5 MB.");
    event.target.value = "";
    return;
  }

  const dataUrl = await readFileAsDataUrl(file);
  profileBuilderDraft.photos[index] = dataUrl;
  renderProfileBuilder();
  event.target.value = "";
}

function readFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result || ""));
    reader.onerror = () => reject(new Error("Could not read the selected image."));
    reader.readAsDataURL(file);
  });
}

async function saveProfileBuilder() {
  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    showToast("Profile builder is unavailable right now.");
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/directory/me/", {
      method: "POST",
      body: {
        skills: profileBuilderDraft.skills,
        hobbies: profileBuilderDraft.hobbiesText,
        interests: profileBuilderDraft.interestsText,
        profile_photos: profileBuilderDraft.photos.filter(Boolean),
      },
    });

    appData.currentProfile = payload.profile || appData.currentProfile;
    appData.profileSkillLibrary = Array.isArray(payload.skill_library)
      ? payload.skill_library
      : appData.profileSkillLibrary;
    profileBuilderDraft = createProfileDraftFromProfile(appData.currentProfile);
    if (appData.currentProfile) {
      const updatedCard = mapDirectoryProfileToCard(appData.currentProfile);
      const index = appData.directory.findIndex((person) => person.sourceUserId === updatedCard.sourceUserId);
      if (index >= 0) {
        appData.directory.splice(index, 1, updatedCard);
      }
    }
    renderProfile();
    renderProfileBuilder();
    renderDirectory();
    showToast("Your profile has been updated.");
  } catch (error) {
    showToast(error.message || "Could not save your profile.");
  }
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
        <button
          type="button"
          class="action-btn ${post.currentUserHasReacted ? "liked" : ""}"
          data-action="toggle-live-reaction"
          data-id="${post.sourceId}"
        >
          ${likeIcon()}${escapeHtml(String(post.reactionCount))}
        </button>
        <button type="button" class="action-btn" data-action="open-live-comments" data-id="${post.sourceId}">
          ${commentIcon()}${escapeHtml(String(post.commentCount))}
        </button>
        <div class="spacer"></div>
        ${renderDeleteLivePostButton(post, "ideas_voice")}
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

function renderRecognitionPostCard(post) {
  return `
    <article class="card voice-card recognition-card recognition-topic-${escapeHtml(post.topic)}" id="${post.id}">
      <div class="voice-card-top">
        <div class="voice-card-tags">
          <span class="mini-chip">${escapeHtml(post.topicLabel)}</span>
          ${post.tagLabel ? `<span class="mini-chip success">${escapeHtml(post.tagLabel)}</span>` : ""}
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
      <div class="recognition-recipient-row">
        <div class="mini-av" style="background:${gradientValue(gradientKeyFromText(post.recipientName || post.title))}">${escapeHtml(post.recipientInitials)}</div>
        <div>
          <div class="mini-item-title">${escapeHtml(post.recipientName || "Acuité team member")}</div>
          <div class="mini-item-meta">${escapeHtml(post.topic === "kudos" ? "Being recognised publicly" : "Being celebrated publicly")}</div>
        </div>
      </div>
      <div class="card-body">
        <div class="card-title">${escapeHtml(post.title)}</div>
        <p>${escapeHtml(post.body)}</p>
      </div>
      <div class="card-actions">
        <button
          type="button"
          class="action-btn ${post.currentUserHasReacted ? "liked" : ""}"
          data-action="toggle-live-reaction"
          data-id="${post.sourceId}"
        >
          ${likeIcon()}${escapeHtml(String(post.reactionCount))}
        </button>
        <button type="button" class="action-btn" data-action="open-live-comments" data-id="${post.sourceId}">
          ${commentIcon()}${escapeHtml(String(post.commentCount))}
        </button>
        <div class="spacer"></div>
        ${renderDeleteLivePostButton(post, "recognition")}
        <button
          type="button"
          class="btn-outline"
          data-action="post-cta"
          data-message="${escapeHtml(`Recognition shared for ${post.recipientName || "a teammate"}.`)}"
        >
          Appreciate
        </button>
      </div>
    </article>
  `;
}

function renderBulletinPostCard(post) {
  return `
    <article class="card voice-card bulletin-card bulletin-category-${escapeHtml(post.category)}" id="${post.id}">
      <div class="voice-card-top">
        <div class="voice-card-tags">
          <span class="mini-chip">${escapeHtml(post.categoryLabel)}</span>
          ${post.templateKey ? `<span class="mini-chip success">${escapeHtml(capitalize(post.templateKey.replaceAll("_", " ")))}</span>` : ""}
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
      ${post.bulletinCard ? renderNativeCelebrationCard(post.bulletinCard) : ""}
      ${
        !post.bulletinCard && post.imageDataUrl
          ? `<div class="bulletin-card-image">
              <img src="${escapeHtml(post.imageDataUrl)}" alt="${escapeHtml(post.imageAlt)}" loading="lazy">
            </div>`
          : ""
      }
      <div class="card-body">
        <div class="card-title">${escapeHtml(post.title)}</div>
        ${post.body.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("")}
      </div>
      ${
        post.metaLines.length
          ? `<div class="bulletin-meta-lines">
              ${post.metaLines.map((line) => `<span class="mini-chip">${escapeHtml(line)}</span>`).join("")}
            </div>`
          : ""
      }
      <div class="card-actions">
        <button
          type="button"
          class="action-btn ${post.currentUserHasReacted ? "liked" : ""}"
          data-action="toggle-live-reaction"
          data-id="${post.sourceId}"
        >
          ${likeIcon()}${escapeHtml(String(post.reactionCount))}
        </button>
        <button type="button" class="action-btn" data-action="open-live-comments" data-id="${post.sourceId}">
          ${commentIcon()}${escapeHtml(String(post.commentCount))}
        </button>
        <div class="spacer"></div>
        ${
          post.ctaLabel && post.ctaTarget
            ? `
              <button
                type="button"
                class="btn-outline"
                data-action="open-bulletin-cta"
                data-target="${escapeHtml(post.ctaTarget)}"
              >
                ${escapeHtml(post.ctaLabel)}
              </button>
            `
            : ""
        }
        ${renderDeleteLivePostButton(post, "general")}
      </div>
    </article>
  `;
}

function renderNativeCelebrationCard(card) {
  const photo = String(card?.photo_url || "").trim();
  return `
    <div class="bulletin-native-card bulletin-style-${escapeHtml(card?.style_key || "sunrise")}">
      <div class="bulletin-native-top">
        <span class="bulletin-native-kicker">${escapeHtml(card?.occasion_label || "Celebration")}</span>
        <span class="bulletin-native-date">${escapeHtml(card?.date_label || "")}</span>
      </div>
      <div class="bulletin-native-person">
        ${
          photo
            ? `<img src="${escapeHtml(photo)}" alt="${escapeHtml(card?.person_name || "Employee")}" class="bulletin-native-photo" loading="lazy">`
            : `<div class="bulletin-native-photo bulletin-native-photo-fallback">${escapeHtml(card?.initials || "AC")}</div>`
        }
        <div>
          <div class="bulletin-native-name">${escapeHtml(card?.person_name || "")}</div>
          <div class="bulletin-native-role">${escapeHtml(card?.person_role || "")}</div>
        </div>
      </div>
      <div class="bulletin-native-message">${escapeHtml(card?.message || "")}</div>
    </div>
  `;
}

function renderDeleteLivePostButton(post, moduleName) {
  if (!post.canDelete) {
    return "";
  }
  return `
    <button
      type="button"
      class="btn-link post-delete-btn"
      data-action="delete-live-post"
      data-id="${post.sourceId}"
      data-module="${moduleName}"
    >
      Delete
    </button>
  `;
}

function updateLivePostFromPayload(postPayload) {
  const replaceMappedPost = (items, mappedPost) => items.map((item) => (
    item.sourceId === mappedPost.sourceId ? mappedPost : item
  ));

  if (postPayload.module === "community") {
    const mapped = mapCommunityPost(postPayload);
    appData.communityPosts = replaceMappedPost(appData.communityPosts, mapped);
    return;
  }

  if (postPayload.module === "ideas_voice") {
    const mapped = mapVoicePost(postPayload);
    appData.voicePosts = replaceMappedPost(appData.voicePosts, mapped);
    return;
  }

  if (postPayload.module === "recognition") {
    const mapped = mapRecognitionPost(postPayload);
    appData.recognitionPosts = replaceMappedPost(appData.recognitionPosts, mapped);
  }
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
