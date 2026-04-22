const STORAGE_KEY = "acuite-connect-state-v2-live";
const DIRECTORY_CACHE_KEY = "acuite-connect-directory-cache-v1";
const CEO_DESK_CACHE_KEY = "acuite-connect-ceo-desk-cache-v1";
const LEARNING_CACHE_KEY = "acuite-connect-library-cache-v1";
const ANNOUNCEMENT_REMINDER_KEY = "acuite-connect-announcement-reminder-v1";

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
const BROCHURE_RESOURCE_PATH = "/static/resources/acuite/acuite-brochure.html";
const IAM_ACUITE_TILE_COUNT = 400;
const IAM_ACUITE_COLUMNS = 25;
const IAM_ACUITE_ROWS = 16;
const IAM_ACUITE_PLACEHOLDER_COLOR = "#7b241c";
const FEED_MODULE_BULLETIN = "bulletin";
const FEED_MODULE_EMPLOYEE_POSTS = "employee_posts";
const FEED_MODULE_COMMUNITY = "community";
const CELEBRATION_TEMPLATE_KEYS = new Set(["birthday_wish", "work_anniversary"]);
const ENABLED_TABS = new Set(["iam-acuite", "home", "holidays", "resources", "brochure-builder", "applications", "knowledge", "ceo-desk", "bulletin", "my-posts", "community", "playtime", "battleship", "quiz", "library", "store", "directory", "profile", "help"]);
const BULLETIN_CATEGORY_LABELS = {
  announcements: "Announcements",
  employee_posts: "Employee posts",
  hr: "HR",
  events: "Events",
  security: "Security",
};
const MY_POST_TYPES = [
  ["looking_for_roommate", "I am looking for a room mate", "Looking for a room mate in Mumbai", "Area, budget or move-in month", "Explain the location, budget, move-in timing, and any other relevant detail."],
  ["give_away", "I want to give away something", "Giving away an office chair", "Condition, pickup location or deadline", "Describe the item, condition, pickup details, and who should contact you."],
  ["exchange_something", "I want to exchange something", "Looking to exchange a study table", "Item, city or expected exchange", "Explain what you have, what you want in return, and how someone should respond."],
  ["share_idea", "I have an idea to share", "Idea to improve internal review sharing", "People, workflow, culture or productivity", "Describe the idea clearly and explain why it would help Acuité."],
  ["share_knowledge", "I have some knowledge to share", "Sharing a sector learning note", "Topic, team or use case", "Explain what you want to share and why it may help colleagues."],
  ["looking_for_guidance", "I am looking for some guidance", "Looking for guidance on transition planning", "Topic, function or experience area", "Explain what guidance you need and what kind of help would be most useful."],
  ["praise_someone", "I want to praise someone", "Appreciation for a colleague", "Team, context or contribution", "Say what the person did and why you think others should know about it."],
  ["organise_training", "I want to organise a training", "Organising a workshop on sector writing", "Topic, audience or possible timing", "Explain the training idea, who it is for, and what support you need."],
  ["looking_for_training", "I am looking for some training", "Looking for training on presentation skills", "Topic, level or team need", "Explain the skill gap and what kind of training would help."],
  ["share_story", "I want to share a story", "A short workplace story", "Theme or setting", "Write your story clearly so the admin can review it before publishing."],
  ["write_book_review", "I want to write a book review", "Book review title", "Book name, author or theme", "Write your book review clearly for admin review."],
  ["write_movie_review", "I want to write a movie review", "Movie review title", "Movie name, genre or theme", "Write your movie review clearly for admin review."],
  ["invite_to_club", "I want to invite people to join a club", "Invitation to join a club", "Club name, theme or activity", "Explain the club, who should join, and how colleagues can participate."],
  ["share_travel", "I want to share about my travel", "A travel note from Ladakh", "Place, season or key highlight", "Share your travel story, key takeaways, and what made the experience memorable."],
].map(([key, label, titlePlaceholder, metaPlaceholder, bodyPlaceholder]) => ({
  key,
  label,
  titleLabel: key === "praise_someone" ? "Select the person" : "What should the post headline say?",
  titlePlaceholder: key === "praise_someone"
    ? "Type the first few letters, then choose from the list"
    : titlePlaceholder,
  metaLabel: key === "praise_someone" ? "Subject Line" : "One short line people should know",
  metaPlaceholder: key === "praise_someone" ? "Add the subject line" : metaPlaceholder,
  bodyLabel: key === "praise_someone"
    ? "Body of the message"
    : key === "share_poem"
      ? "Poem"
      : key === "share_story"
        ? "Story"
        : "Details",
  bodyPlaceholder: key === "praise_someone"
    ? "Write the message clearly."
    : bodyPlaceholder,
  inputMode: key === "praise_someone" ? "person_picker" : "standard",
  hideHelpCopy: key === "praise_someone",
}));
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

function getCurrentBuildNumber() {
  const buildDisplay = document.getElementById("build-number-display");
  if (!buildDisplay) {
    return "";
  }
  const match = String(buildDisplay.textContent || "").match(/BUILD\s+([0-9.]+)/i);
  return match ? match[1] : "";
}
const DEFAULT_CEO_DESK_MESSAGE = {
  date: "April 21, 2026",
  title: "Welcome to Acuité Connect",
  meta: "A new digital space for our people to connect, engage and participate",
  body: [
    "Hello Team,",
    "I am pleased to introduce Acuité Connect, our new internal platform created to bring our people, ideas and communication together in one place.",
    "As we continue to grow, it becomes more important for all of us to stay connected, informed and engaged with one another. Acuité Connect has been built to serve as our shared digital workplace where employees can see important announcements, hear directly from leadership, connect with colleagues, participate in discussions, access resources, and contribute meaningfully to the culture of our organisation.",
    "This platform is meant to make communication more open, structured and accessible. It is also intended to create a stronger sense of community across teams, functions and locations. Whether you want to stay updated, reach out to leadership, celebrate colleagues, explore resources or participate in employee activities, Acuité Connect is designed to support that experience.",
    "I encourage each of you to explore the platform and use it actively and responsibly. The value of Acuité Connect will come not only from the features it offers, but from the way we as a team use it to share, learn, recognise and engage with each other.",
    "I hope this becomes a meaningful and useful space for all of us.",
    "Cheers!\nSankar",
  ],
};
const DEFAULT_CEO_DESK_ARCHIVE = [
  {
    datePosted: "March 31, 2026",
    headline: "Hola FY2027",
    subjectLine: "A steady view on performance, priorities, and the path ahead.",
    body: [
      "Dear colleagues,",
      "As we close another financial year, it is important for all of us to pause and look at both performance and purpose. The year behind us demanded discipline, teamwork, and calm judgement. Across functions and offices, many of you carried that responsibility with seriousness. I want to acknowledge that effort.",
      "The year ahead now asks us for equal clarity. We must continue strengthening analytical quality, improving operating rhythm, and building a stronger internal culture of ownership. Growth matters, but credible growth matters more. We will therefore stay focused on quality, client trust, and internal capability-building together.",
      "Connect is meant to support that culture. It should not only inform employees, but also make it easier for ideas, questions, and thoughtful suggestions to reach leadership in a structured way. I encourage you to use that access well. Ask what should be improved. Share what should be protected. Suggest what should be built next.",
      "Thank you for the work you do, and for the seriousness with which you do it.",
      "Cheers!\nSankar",
    ],
  },
];
const BULLETIN_BOARD_RETENTION_DAYS = 30;
const CEO_DESK_ARCHIVE_LIMIT = 12;
const COMPANY_HOLIDAY_CALENDAR = [
  { date: "2026-04-14", label: "Tamil New Year", applicability: "Chennai" },
  { date: "2026-05-01", label: "Maharashtra Day", applicability: "All Offices" },
  { date: "2026-06-02", label: "Telangana Foundation Day", applicability: "Hyderabad" },
  { date: "2026-08-15", label: "Independence Day", applicability: "All Offices" },
  { date: "2026-09-04", label: "Janmashtami", applicability: "Delhi" },
  { date: "2026-09-14", label: "Ganesh Chaturthi", applicability: "Mumbai, Chennai, Hyderabad, Bangalore, Ahmedabad" },
  { date: "2026-10-02", label: "Gandhi Jayanti", applicability: "All Offices" },
  { date: "2026-10-19", label: "Durgapuja Nabami", applicability: "Kolkata" },
  { date: "2026-10-20", label: "Dussehra", applicability: "All Offices" },
  { date: "2026-11-01", label: "Karnataka Day", applicability: "Bangalore" },
  { date: "2026-11-08", label: "Diwali (Laxmi Pujan)", applicability: "All Offices" },
  { date: "2026-11-10", label: "Vikram Samvat New Year", applicability: "Ahmedabad" },
  { date: "2026-11-24", label: "Guru Nanak Jayanti", applicability: "Delhi" },
  { date: "2026-12-25", label: "Christmas", applicability: "All Offices" },
];
const COMPANY_EVENT_CALENDAR = [
  {
    date: "2026-04-23",
    label: "Town hall and leadership briefing",
  },
];

const COMMUNITY_CLUB_EMOJIS = {
  reading_club: "📚",
  movie_club: "🎬",
  travel_club: "✈️",
  entertainment_club: "🎭",
  quiz_club: "🧠",
  debate_club: "🎙️",
  technology_club: "💻",
  photography_club: "📷",
  cricket_club: "🏏",
  football_club: "⚽",
  charity_club: "🤝",
  health_club: "💚",
};

const HOME_ANNOUNCEMENT_FILTERS = [
  ["leadership", "Leadership"],
  ["people_culture", "People & Culture"],
  ["cybersecurity", "Cybersecurity"],
  ["compliance", "Compliance"],
  ["regulations", "Regulations"],
  ["new_initiatives", "New Initiatives"],
  ["giving", "Giving"],
  ["opinion_poll", "Opinion Poll"],
];

const HOME_ANNOUNCEMENTS = [
  {
    id: "announcement-townhall-launch",
    tag: "leadership",
    eyebrow: "Priority Announcement",
    type: "Town Hall",
    format: "Hybrid",
    title: "Town hall and leadership briefing.",
    summary: "How did we do last year? What is our plan going forward? If you want to know about these, do attend the session. Before the session you may post a question to our MD & CEO, give a suggestion or share an idea.",
    dateLabel: "Wednesday, 6th May 2026",
    timeLabel: "4:00 PM - 5:30 PM IST",
    venueLabel: "Venue: TBD",
    hostLabel: "Hosted by the MD & CEO with the leadership team",
    audienceLabel: "Open to all employees",
    countdownLabel: getTownHallCountdownLabel("2026-05-06"),
    baseMetrics: {
      likes: 96,
    },
  },
];
const TOWN_HALL_GENERIC_CONTENT = {
  title: "Town hall and leadership briefing.",
  summary: "How did we do last year? What is our plan going forward? If you want to know about these, do attend the session. Before the session you may post a question to our MD & CEO, give a suggestion or share an idea.",
  hostLabel: "Hosted by the MD & CEO with the leadership team",
  audienceLabel: "Open to all employees",
};
const CEO_DESK_EDITORIAL = {
  id: "ceo-desk-editorial-april-2026",
  baseLikes: 24,
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
  currentUserPoints: 0,
  rewardRules: [],
  storeItems: [],
  storeRedemptions: [],
  storeBalance: {
    earned_points: 0,
    locked_points: 0,
    spent_points: 0,
    expired_points: 0,
    available_points: 0,
    register: [],
  },
  storeCoinRules: [],
  adminUsers: [],
  learningBooks: [],
  learningRequisitions: [],
  homeAnnouncementPosts: [],
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
  birthdays: [
    { id: "birthday-sneha", name: "Sneha Patil", date: "Today!", initials: "SP", gradient: "cool", highlight: true },
    { id: "birthday-amit", name: "Amit Kumar", date: "Mar 24", initials: "AK", gradient: "warm", highlight: false },
    { id: "birthday-riya", name: "Riya Desai", date: "Mar 26", initials: "RD", gradient: "sun", highlight: false },
  ],
  anniversaries: [
    { id: "anniversary-priya", name: "Priya Sharma", date: "5 years", initials: "PS", gradient: "fire", highlight: true },
    { id: "anniversary-vikram", name: "Vikram Joshi", date: "3 yrs - Mar 25", initials: "VJ", gradient: "cool", highlight: false },
  ],
};

Object.assign(appData, {
  currentProfile: null,
  profileSkillLibrary: [],
  currentUserPoints: 0,
  rewardRules: [],
  storeItems: [],
  storeRedemptions: [],
  storeBalance: {
    earned_points: 0,
    locked_points: 0,
    spent_points: 0,
    expired_points: 0,
    available_points: 0,
    register: [],
  },
  storeCoinRules: [],
  adminUsers: [],
  learningBooks: [],
  learningRequisitions: [],
  homePosts: [],
  bulletinPosts: [],
  ceoDeskPosts: [],
  myPosts: [],
  communityClubs: [],
  communityPostsByClub: {},
  directory: [],
  birthdays: [],
  anniversaries: [],
});

let directoryFilterOptions = createDirectoryFilterOptions();

const defaultState = {
  theme: "",
  activeTab: "home",
  homeAnnouncementFilter: "leadership",
  brochureBuilderSelectedIds: [],
  storeFilter: "all",
  learningBookFilter: "all",
  learningBookQuery: "",
  bulletinFilter: "all",
  communityClubKey: "",
  directoryFilters: createDirectoryFiltersState(),
  directoryQuery: "",
  likedPostIds: [],
  customBulletins: [],
};

let state = hydrateState();
let elements = {};
let latestSearchResults = [];
let toastTimeoutId = null;
let directoryLoadError = "";
let directoryCachedAt = "";
let directoryShowingCachedData = false;
let iamAcuitePosterState = {
  signature: "",
  dataUrl: "",
  photoCount: 0,
  loading: false,
  error: "",
};
let iamAcuiteRenderToken = 0;
let ceoDeskCachedAt = "";
let ceoDeskShowingCachedData = false;
let learningCachedAt = "";
let learningShowingCachedData = false;
let storeLoadError = "";
let learningLoadError = "";
let bulletinLoadError = "";
let selectedCeoDeskArchiveKey = "";
let myPostsLoadError = "";
let adminUsersLoadError = "";
let communityLoadError = "";
let communityLoading = false;
let communityPostsLoadingKey = "";
let communityPostsSubmittingKey = "";
let communityPostsErrorByClub = {};
let profileBuilderLoadError = "";
let profileBuilderDraft = createProfileBuilderDraft();
let profileMenuOpen = false;
let activeCommentsPostId = 0;
let liveComments = [];
let liveCommentsError = "";
let liveCommentsLoading = false;
let brochureSlides = [];
let brochureLoadError = "";
let brochureSlidesLoading = false;
let brochurePresentationOpen = false;
let brochurePresentationIndex = 0;
let brochurePresentationSignature = "";
let brochurePresentationHudTimer = null;
let brochurePresentationHintTimer = null;
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

function safeRender(label, renderFn) {
  try {
    renderFn();
  } catch (error) {
    console.error(`Could not render ${label}.`, error);
  }
}

function renderShell() {
  safeRender("panels", renderPanels);
  safeRender("profile", renderProfile);
  safeRender("profile builder", renderProfileBuilder);
  safeRender("brochure builder", renderBrochureBuilderPanel);
  safeRender("brochure presentation", renderBrochurePresentation);
  safeRender("comments modal", renderCommentsModal);
  safeRender("composer access", syncComposerAccess);
  safeRender("community panel", renderCommunityPanel);
  safeRender("home announcement", renderHomeAnnouncement);
  safeRender("holiday panel", renderHolidayPanel);
  safeRender("birthdays", renderBirthdays);
  safeRender("anniversaries", renderAnniversaries);
  safeRender("sidebar holidays", renderSidebarHolidays);
  safeRender("sidebar events", renderSidebarEvents);
  safeRender("CEO desk like button", renderCeoDeskLikeButton);
  safeRender("filter buttons", syncFilterButtons);
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
    adminSidebarTab: document.getElementById("admin-sidebar-tab"),
    bulletinAdminOpenButton: document.getElementById("bulletin-admin-open-btn"),
    myPostsForm: document.getElementById("my-posts-form"),
    myPostsTypeSelect: document.getElementById("my-posts-type-select"),
    myPostsFields: document.getElementById("my-posts-fields"),
    myPostsTitleLabel: document.getElementById("my-posts-title-label"),
    myPostsTitleInput: document.getElementById("my-posts-title-input"),
    myPostsSelectedPersonId: document.getElementById("my-posts-selected-person-id"),
    myPostsPersonSuggestions: document.getElementById("my-posts-person-suggestions"),
    myPostsMetaLabel: document.getElementById("my-posts-meta-label"),
    myPostsMetaInput: document.getElementById("my-posts-meta-input"),
    myPostsBodyLabel: document.getElementById("my-posts-body-label"),
    myPostsBodyInput: document.getElementById("my-posts-body-input"),
    myPostsHelpCopy: document.getElementById("my-posts-help-copy"),
    myPostsList: document.getElementById("my-posts-list"),
    myPostsResultsMeta: document.getElementById("my-posts-results-meta"),
    communityGrid: document.getElementById("community-grid"),
    communityResultsMeta: document.getElementById("community-results-meta"),
    communityWorkspace: document.getElementById("community-workspace"),
    communityWorkspaceBody: document.getElementById("community-workspace-body"),
    brochureBuilderMeta: document.getElementById("brochure-builder-meta"),
    brochurePickerList: document.getElementById("brochure-picker-list"),
    brochureSelectionMeta: document.getElementById("brochure-selection-meta"),
    brochurePreviewList: document.getElementById("brochure-preview-list"),
    brochurePresentationBackdrop: document.getElementById("brochure-presentation-backdrop"),
    brochurePresentationMeta: document.getElementById("brochure-presentation-meta"),
    brochurePresentationMain: document.getElementById("brochure-presentation-main"),
    brochurePresentationHud: document.getElementById("brochure-presentation-hud"),
    brochurePresentationHint: document.getElementById("brochure-presentation-hint"),
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
    profileBuilderForm: document.getElementById("profile-builder-form"),
    profileMenu: document.getElementById("profile-menu"),
    profileModalBackdrop: document.getElementById("profile-modal-backdrop"),
    commentsModalBackdrop: document.getElementById("comments-modal-backdrop"),
    announcementReminderBackdrop: document.getElementById("announcement-reminder-backdrop"),
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
  showAnnouncementReminderIfNeeded();
  const hydratedDirectoryCache = hydrateDirectoryCache();
  if (state.activeTab === "directory" && hydratedDirectoryCache) {
    renderAll();
  }
  const hydratedCeoDeskCache = hydrateCeoDeskCache();
  if (state.activeTab === "ceo-desk" && hydratedCeoDeskCache) {
    renderAll();
  }
  const hydratedLearningCache = hydrateLearningCache();
  if (state.activeTab === "library" && hydratedLearningCache) {
    renderAll();
  }

  try {
    const criticalTasks = [
      loadCurrentProfile(),
      loadCommunityData(),
      loadHomeAnnouncementPosts(),
      loadBulletinPosts(),
      loadCeoDeskPosts(),
      loadMyPosts(),
      loadStoreData(),
      loadRecognitionData(),
    ];
    await Promise.allSettled(criticalTasks);
    renderAll();
    void Promise.allSettled([
      loadDirectoryData(),
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
  const hasCachedDirectory = hydrateDirectoryCache();
  if (!hasCachedDirectory) {
    directoryFilterOptions = createDirectoryFilterOptions();
    appData.directory = [];
    directoryCachedAt = "";
    directoryShowingCachedData = false;
  }

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
    directoryCachedAt = new Date().toISOString();
    directoryShowingCachedData = false;
    saveDirectoryCache();
    invalidateIamAcuitePoster();
  } catch (error) {
    directoryLoadError = hasCachedDirectory
      ? ""
      : (error.message || "Could not load the people directory.");
  }
}

async function loadLearningData() {
  learningLoadError = "";
  const hasCachedLearning = hydrateLearningCache();
  if (!hasCachedLearning) {
    appData.learningBooks = [];
    appData.learningRequisitions = [];
    learningCachedAt = "";
    learningShowingCachedData = false;
  }

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    learningLoadError = "Learning services are unavailable in this build.";
    return;
  }

  try {
    const booksPayload = await window.AcuiteConnectAuth.apiRequest("/api/learning/books/");
    appData.learningBooks = Array.isArray(booksPayload.results) ? booksPayload.results : [];
    learningCachedAt = new Date().toISOString();
    learningShowingCachedData = false;
    saveLearningCache();
  } catch (error) {
    learningLoadError = hasCachedLearning
      ? ""
      : (error.message || "Could not load book-club data.");
  }
}

async function loadRecognitionData() {
  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    appData.birthdays = [];
    appData.anniversaries = [];
    appData.currentUserPoints = 0;
    appData.rewardRules = [];
    return;
  }

  try {
    const overviewPayload = await window.AcuiteConnectAuth.apiRequest("/api/recognition/overview/");
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
  } catch (error) {
    appData.birthdays = [];
    appData.anniversaries = [];
    appData.currentUserPoints = 0;
    appData.rewardRules = [];
  }
}

async function loadStoreData() {
  storeLoadError = "";
  appData.storeItems = [];
  appData.storeRedemptions = [];
  appData.storeBalance = {
    earned_points: 0,
    locked_points: 0,
    spent_points: 0,
    expired_points: 0,
    available_points: 0,
    register: [],
  };
  appData.storeCoinRules = [];

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    storeLoadError = "Brand Store services are unavailable in this build.";
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/store/overview/");
    appData.storeItems = Array.isArray(payload.items) ? payload.items : [];
    appData.storeRedemptions = Array.isArray(payload.my_redemptions) ? payload.my_redemptions : [];
    appData.storeBalance = payload.balance || appData.storeBalance;
    appData.storeCoinRules = Array.isArray(payload.coin_rules) ? payload.coin_rules : [];
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
    const [employeePostsPayload, celebrationPostsPayload] = await Promise.all([
      window.AcuiteConnectAuth.apiRequest(
        `/api/feed/posts/?module=${FEED_MODULE_EMPLOYEE_POSTS}&topic=employee_submission`,
      ),
      window.AcuiteConnectAuth.apiRequest(
        `/api/feed/posts/?module=${FEED_MODULE_BULLETIN}&topic=hr`,
      ),
    ]);
    const employeeResults = Array.isArray(employeePostsPayload.results)
      ? employeePostsPayload.results
        .map(mapBulletinPost)
        .filter((post) => post.userSubmission)
      : [];
    const celebrationResults = Array.isArray(celebrationPostsPayload.results)
      ? celebrationPostsPayload.results
        .map(mapBulletinPost)
        .filter((post) => isCelebrationBulletinPost(post))
      : [];
    appData.bulletinPosts = sortBulletinPostsNewestFirst([...employeeResults, ...celebrationResults]);
  } catch (error) {
    bulletinLoadError = error.message || "Could not load the Bulletin Board.";
  }
}

async function loadHomeAnnouncementPosts() {
  appData.homeAnnouncementPosts = [];

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest(
      `/api/feed/posts/?module=${FEED_MODULE_BULLETIN}&home_announcements=1`,
    );
    appData.homeAnnouncementPosts = Array.isArray(payload.results)
      ? sortBulletinPostsNewestFirst(payload.results.map(mapBulletinPost))
      : [];
  } catch (error) {
    appData.homeAnnouncementPosts = [];
  }
}

async function loadCeoDeskPosts() {
  const hasCachedCeoDesk = hydrateCeoDeskCache();
  if (!hasCachedCeoDesk) {
    appData.ceoDeskPosts = [];
    ceoDeskCachedAt = "";
    ceoDeskShowingCachedData = false;
  }

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest(
      `/api/feed/posts/?module=${FEED_MODULE_BULLETIN}&bulletin_channel=ceo_desk`,
    );
    appData.ceoDeskPosts = Array.isArray(payload.results)
      ? sortBulletinPostsNewestFirst(payload.results.map(mapBulletinPost))
      : [];
    ceoDeskCachedAt = new Date().toISOString();
    ceoDeskShowingCachedData = false;
    saveCeoDeskCache();
  } catch (error) {
    if (!hasCachedCeoDesk) {
      appData.ceoDeskPosts = [];
    }
  }
}

async function loadMyPosts() {
  myPostsLoadError = "";
  appData.myPosts = [];

  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest || !appData.currentUser?.id) {
    myPostsLoadError = "My Posts is unavailable in this build.";
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest(
      `/api/feed/posts/?module=${FEED_MODULE_EMPLOYEE_POSTS}&topic=employee_submission&author_id=${encodeURIComponent(String(appData.currentUser.id))}`,
    );
    appData.myPosts = Array.isArray(payload.results)
      ? payload.results.map(mapMyPostSubmission)
      : [];
  } catch (error) {
    myPostsLoadError = error.message || "Could not load your submitted posts.";
  }
}

async function loadCommunityData() {
  if (communityLoading) {
    return;
  }

  communityLoading = true;
  communityLoadError = "";
  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/directory/communities/");
    appData.communityClubs = Array.isArray(payload.results) ? payload.results : [];
    syncActiveCommunityClub();
    if (appData.currentProfile) {
      appData.currentProfile.clubs = Array.isArray(payload.my_clubs) ? payload.my_clubs : [];
    }
  } catch (error) {
    communityLoadError = error.message || "Could not load communities.";
  } finally {
    communityLoading = false;
    renderCommunityPanel();
  }
}

function syncActiveCommunityClub() {
  const availableKeys = appData.communityClubs.map((club) => club.key);
  if (state.communityClubKey && availableKeys.includes(state.communityClubKey)) {
    return;
  }
  const preferredClub = appData.communityClubs.find((club) => club.joined) || appData.communityClubs[0];
  state.communityClubKey = preferredClub?.key || "";
  saveState();
}

function getActiveCommunityClub() {
  syncActiveCommunityClub();
  return appData.communityClubs.find((club) => club.key === state.communityClubKey) || null;
}

function setActiveCommunityClub(clubKey) {
  const nextKey = String(clubKey || "").trim();
  if (!nextKey) {
    return;
  }
  state.communityClubKey = nextKey;
  saveState();
  renderCommunityPanel();
  const club = getActiveCommunityClub();
  if (club?.joined) {
    void loadCommunityPosts(club.key);
  }
}

async function loadCommunityPosts(clubKey, { force = false } = {}) {
  const normalizedClubKey = String(clubKey || "").trim();
  if (!normalizedClubKey || communityPostsLoadingKey === normalizedClubKey) {
    return;
  }
  if (!force && Array.isArray(appData.communityPostsByClub[normalizedClubKey])) {
    return;
  }
  if (!window.AcuiteConnectAuth || !window.AcuiteConnectAuth.apiRequest) {
    communityPostsErrorByClub[normalizedClubKey] = "Community feed is unavailable in this build.";
    renderCommunityPanel();
    return;
  }

  communityPostsLoadingKey = normalizedClubKey;
  delete communityPostsErrorByClub[normalizedClubKey];
  renderCommunityPanel();
  try {
    const payload = await window.AcuiteConnectAuth.apiRequest(
      `/api/feed/posts/?module=${FEED_MODULE_COMMUNITY}&topic=${encodeURIComponent(normalizedClubKey)}&limit=100`,
    );
    appData.communityPostsByClub[normalizedClubKey] = Array.isArray(payload.results)
      ? payload.results.map(mapCommunityPost)
      : [];
  } catch (error) {
    communityPostsErrorByClub[normalizedClubKey] = error.message || "Could not load club posts.";
  } finally {
    if (communityPostsLoadingKey === normalizedClubKey) {
      communityPostsLoadingKey = "";
    }
    renderCommunityPanel();
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
  document.addEventListener("change", handleDocumentChange);
  document.addEventListener("keydown", handleDocumentKeydown);
  document.addEventListener("fullscreenchange", handleDocumentFullscreenChange);
  document.addEventListener("submit", handleSubmit);
  window.addEventListener("resize", handleWindowResize);

  if (elements.searchInput) {
    elements.searchInput.addEventListener("input", handleSearchInput);
    elements.searchInput.addEventListener("keydown", handleSearchKeydown);
    elements.searchInput.addEventListener("focus", () => {
      if (elements.searchInput.value.trim()) {
        updateSearchResults(elements.searchInput.value.trim());
      }
    });
  }

  if (elements.myPostsTypeSelect) {
    elements.myPostsTypeSelect.addEventListener("change", () => {
      syncMyPostsComposer();
    });
  }

  if (elements.myPostsTitleInput) {
    elements.myPostsTitleInput.addEventListener("input", () => {
      handleMyPostsTitleInput();
    });
    elements.myPostsTitleInput.addEventListener("focus", () => {
      renderMyPostsPersonSuggestions();
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

  const homeAnnouncementTypeSelect = document.getElementById("home-announcement-type-select");
  if (homeAnnouncementTypeSelect) {
    homeAnnouncementTypeSelect.addEventListener("change", () => {
      syncHomeAnnouncementAdminForm();
    });
  }

  elements.directorySearchInput.addEventListener("input", (event) => {
    state.directoryQuery = event.target.value;
    saveState();
    renderDirectory();
  });

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

    if (actionName === "set-home-announcement-filter") {
      state.homeAnnouncementFilter = action.dataset.filter || "leadership";
      saveState();
      renderHomeAnnouncement();
      renderHomeAnnouncementFilters();
      return;
    }

    if (actionName === "open-launcher") {
      switchTab("bulletin");
      showToast("Jumped to the Bulletin Board.");
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

    if (actionName === "open-help-page") {
      closeProfileMenu();
      switchTab("help");
      return;
    }

    if (actionName === "open-terms-page") {
      closeProfileMenu();
      window.location.href = "/terms-and-conditions.html";
      return;
    }

    if (actionName === "print-brochure-selection") {
      printSelectedBrochureSlides();
      return;
    }

    if (actionName === "present-brochure-selection") {
      openBrochurePresentation();
      return;
    }

    if (actionName === "close-brochure-presentation") {
      closeBrochurePresentation();
      return;
    }

    if (actionName === "open-admin-console") {
      closeProfileMenu();
      window.location.href = "/admin-console.html";
      return;
    }

    if (actionName === "select-my-posts-person") {
      selectMyPostsPerson(action.dataset.id);
      return;
    }

    if (actionName === "select-community-club") {
      setActiveCommunityClub(action.dataset.clubKey);
      return;
    }

    if (actionName === "prefill-ceo-request") {
      prefillCeoDeskComment(action.dataset.requestMessage);
      return;
    }

    if (actionName === "open-ceo-archive-message") {
      const archiveKey = String(action.dataset.archiveKey || "").trim();
      selectedCeoDeskArchiveKey = selectedCeoDeskArchiveKey === archiveKey ? "" : archiveKey;
      renderCeoDeskMessage();
      renderCeoDeskLikeButton();
      scrollCeoDeskMessageIntoView();
      return;
    }

    if (actionName === "return-ceo-current-message") {
      selectedCeoDeskArchiveKey = "";
      renderCeoDeskMessage();
      renderCeoDeskLikeButton();
      scrollCeoDeskMessageIntoView();
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

    if (actionName === "close-announcement-reminder") {
      closeAnnouncementReminder();
      return;
    }

    if (actionName === "toggle-profile-skill") {
      toggleProfileSkill(action.dataset.skill);
      return;
    }

    if (actionName === "toggle-profile-hobby") {
      toggleProfileHobby(action.dataset.hobby);
      return;
    }

    if (actionName === "clear-profile-photo") {
      await clearProfilePhoto(Number(action.dataset.index));
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

    if (actionName === "toggle-book-like") {
      await toggleBookLike(action.dataset.id);
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

    if (actionName === "redeem-store-item") {
      await redeemStoreItem(action.dataset.id);
      return;
    }

    if (actionName === "delete-store-item") {
      await deleteStoreItem(action.dataset.id);
      return;
    }

    if (actionName === "jump-to-item") {
      jumpToItem(action.dataset.tab, action.dataset.targetId);
      return;
    }

    if (actionName === "show-person") {
      showToast(`Expertise profile for ${action.dataset.name} can open from here in the next iteration.`);
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

    if (actionName === "refresh-iam-acuite") {
      void refreshIamAcuitePoster();
      return;
    }

    if (actionName === "placeholder-comment") {
      showToast("Comments can be attached once the backend layer is in place.");
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

  if (brochurePresentationOpen && isBrochurePresenting()) {
    if (event.target.closest(".brochure-presentation-hud, .brochure-presentation-hint, .brochure-presentation-topbar")) {
      return;
    }
    if (event.target.closest(".brochure-presentation-slide") || event.target === elements.brochurePresentationBackdrop || event.target === elements.brochurePresentationMain) {
      moveBrochurePresentation(1);
      return;
    }
  }

  if (!event.target.closest(".profile-menu-shell")) {
    closeProfileMenu();
  }

  if (!event.target.closest(".topnav-search") || !elements.searchResults) {
    hideSearchResults();
  }

  if (
    elements.myPostsPersonSuggestions
    && !elements.myPostsPersonSuggestions.hidden
    && !event.target.closest("#my-posts-person-suggestions")
    && event.target !== elements.myPostsTitleInput
  ) {
    hideMyPostsPersonSuggestions();
  }
}

function handleDocumentChange(event) {
  const brochureCheckbox = event.target.closest("[data-brochure-slide-checkbox]");
  if (brochureCheckbox) {
    toggleBrochureSlideSelection(brochureCheckbox.dataset.brochureSlideCheckbox, brochureCheckbox.checked);
  }
}

function handleDocumentKeydown(event) {
  if (event.key === "Escape" && elements.announcementReminderBackdrop && !elements.announcementReminderBackdrop.hidden) {
    event.preventDefault();
    closeAnnouncementReminder();
    return;
  }

  if (!brochurePresentationOpen) {
    return;
  }

  switch (event.key) {
    case "Escape":
      event.preventDefault();
      closeBrochurePresentation();
      return;
    case "ArrowRight":
    case "PageDown":
    case " ":
    case "Enter":
      event.preventDefault();
      moveBrochurePresentation(1);
      return;
    case "ArrowLeft":
    case "PageUp":
    case "Backspace":
      event.preventDefault();
      moveBrochurePresentation(-1);
      return;
    case "Home":
      event.preventDefault();
      setBrochurePresentationCurrent(0);
      return;
    case "End":
      event.preventDefault();
      setBrochurePresentationCurrent(getBrochurePresentationSlides().length - 1);
      return;
    default:
      return;
  }
}

function handleDocumentFullscreenChange() {
  if (!brochurePresentationOpen) {
    return;
  }

  if (!document.fullscreenElement && isBrochurePresenting()) {
    closeBrochurePresentation({ skipFullscreenExit: true });
    return;
  }

  if (isBrochurePresenting()) {
    const slides = getBrochurePresentationSlides();
    const currentSlide = slides[brochurePresentationIndex];
    if (currentSlide) {
      window.requestAnimationFrame(() => {
        scaleBrochurePresentationIframe(currentSlide);
      });
    }
  }
}

function handleWindowResize() {
  if (!brochurePresentationOpen || !isBrochurePresenting()) {
    return;
  }

  const slides = getBrochurePresentationSlides();
  const currentSlide = slides[brochurePresentationIndex];
  if (currentSlide) {
    window.requestAnimationFrame(() => {
      scaleBrochurePresentationIframe(currentSlide);
    });
  }
}

function handleSubmit(event) {
  if (event.target === elements.myPostsForm) {
    event.preventDefault();
    void submitMyPost();
    return;
  }

  if (event.target.id === "community-post-form") {
    event.preventDefault();
    void submitCommunityPost(event.target);
    return;
  }

  if (event.target.id === "ceo-desk-comment-form") {
    event.preventDefault();
    void submitCeoDeskComment(event.target);
    return;
  }

  if (event.target.id === "ceo-desk-post-form") {
    event.preventDefault();
    void submitCeoDeskPost(event.target);
    return;
  }

  if (event.target.id === "home-announcement-feedback-form") {
    event.preventDefault();
    void submitHomeAnnouncementFeedback(event.target);
    return;
  }

  if (event.target.id === "home-announcement-admin-form") {
    event.preventDefault();
    void submitHomeAnnouncementAdminPost(event.target);
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
  safeRender("theme", applyTheme);
  safeRender("panels", renderPanels);
  safeRender("profile", renderProfile);
  safeRender("profile coin bank", renderProfileCoinBank);
  safeRender("profile builder", renderProfileBuilder);
  safeRender("I am Acuite panel", renderIamAcuitePanel);
  safeRender("brochure builder", renderBrochureBuilderPanel);
  safeRender("brochure presentation", renderBrochurePresentation);
  safeRender("comments modal", renderCommentsModal);
  safeRender("composer access", syncComposerAccess);
  safeRender("CEO desk message", renderCeoDeskMessage);
  safeRender("home announcement", renderHomeAnnouncement);
  safeRender("holiday panel", renderHolidayPanel);
  safeRender("store panel", renderStorePanel);
  safeRender("library panel", renderLearningPanel);
  safeRender("bulletin panel", renderBulletinPanel);
  safeRender("my posts panel", renderMyPostsPanel);
  safeRender("community panel", renderCommunityPanel);
  safeRender("admin panel", renderAdminPanel);
  if (state.activeTab === "directory") {
    safeRender("directory filters", renderDirectoryChips);
    safeRender("directory", renderDirectory);
  }
  safeRender("birthdays", renderBirthdays);
  safeRender("anniversaries", renderAnniversaries);
  safeRender("sidebar holidays", renderSidebarHolidays);
  safeRender("sidebar events", renderSidebarEvents);
  safeRender("CEO desk like button", renderCeoDeskLikeButton);
  safeRender("filter buttons", syncFilterButtons);
}

function renderBrochureBuilderPanel() {
  if (!elements.brochurePickerList || !elements.brochurePreviewList) {
    return;
  }

  if (!brochureSlides.length && !brochureSlidesLoading && !brochureLoadError) {
    void ensureBrochureSlidesLoaded();
  }

  if (elements.brochureBuilderMeta) {
    elements.brochureBuilderMeta.textContent = brochureSlidesLoading
      ? "Loading brochure slides..."
      : brochureLoadError
        ? brochureLoadError
        : brochureSlides.length
          ? `${brochureSlides.length} slides available`
          : "No brochure slides found.";
  }

  if (brochureLoadError) {
    elements.brochurePickerList.innerHTML = `<div class="brochure-preview-empty">${escapeHtml(brochureLoadError)}</div>`;
  } else if (brochureSlidesLoading && !brochureSlides.length) {
    elements.brochurePickerList.innerHTML = '<div class="brochure-preview-empty">Loading brochure slides...</div>';
  } else {
    elements.brochurePickerList.innerHTML = brochureSlides.map((slide) => {
      const orderIndex = state.brochureBuilderSelectedIds.indexOf(slide.id);
      const isSelected = orderIndex >= 0;
      return `
        <label class="brochure-slide-option ${isSelected ? "selected" : ""}">
          <input
            type="checkbox"
            data-brochure-slide-checkbox="${escapeHtml(slide.id)}"
            ${isSelected ? "checked" : ""}
          >
          <div class="brochure-slide-copy">
            <div class="brochure-slide-order">${isSelected ? `Selected #${orderIndex + 1}` : `Slide ${escapeHtml(slide.number)}`}</div>
            <div class="brochure-slide-name">${escapeHtml(slide.name)}</div>
            <div class="brochure-slide-meta">${escapeHtml(slide.rawLabel)}</div>
          </div>
        </label>
      `;
    }).join("");
  }

  const selectedSlides = getSelectedBrochureSlides();
  if (elements.brochureSelectionMeta) {
    elements.brochureSelectionMeta.textContent = selectedSlides.length
      ? `${selectedSlides.length} slide${selectedSlides.length === 1 ? "" : "s"} selected in click order`
      : "Choose one or more slides from the left.";
  }

  if (!selectedSlides.length) {
    elements.brochurePreviewList.innerHTML = `
      <div class="brochure-preview-empty">
        Select slides on the left. They will appear here in the exact order you click them.
      </div>
    `;
    return;
  }

  elements.brochurePreviewList.innerHTML = selectedSlides.map((slide, index) => `
    <article class="brochure-preview-card">
      <div class="brochure-preview-headline">
        <strong>${index + 1}. ${escapeHtml(slide.name)}</strong>
        <span class="mini-item-meta">Slide ${escapeHtml(slide.number)}</span>
      </div>
      <iframe
        class="brochure-preview-frame"
        title="${escapeHtml(`Brochure preview ${slide.number}`)}"
        data-brochure-preview-id="${escapeHtml(slide.id)}"
        loading="lazy"
      ></iframe>
    </article>
  `).join("");

  hydrateBrochureFrames(elements.brochurePreviewList, selectedSlides);
}

function renderBrochurePresentation() {
  if (!elements.brochurePresentationBackdrop || !elements.brochurePresentationMain || !elements.brochurePresentationMeta || !elements.brochurePresentationHud || !elements.brochurePresentationHint) {
    return;
  }

  if (!brochurePresentationOpen) {
    elements.brochurePresentationBackdrop.hidden = true;
    brochurePresentationSignature = "";
    syncModalState();
    return;
  }

  const selectedSlides = getSelectedBrochureSlides();
  if (!selectedSlides.length) {
    closeBrochurePresentation({ skipFullscreenExit: true });
    return;
  }

  const signature = selectedSlides.map((slide) => slide.id).join("|");
  if (brochurePresentationIndex >= selectedSlides.length) {
    brochurePresentationIndex = selectedSlides.length - 1;
  }
  if (brochurePresentationIndex < 0) {
    brochurePresentationIndex = 0;
  }

  elements.brochurePresentationBackdrop.hidden = false;
  elements.brochurePresentationMeta.textContent = `${selectedSlides.length} slide${selectedSlides.length === 1 ? "" : "s"} selected`;
  if (signature !== brochurePresentationSignature) {
    elements.brochurePresentationMain.innerHTML = selectedSlides.map((slide, index) => `
      <section class="brochure-presentation-slide" aria-label="${escapeHtml(`Slide ${index + 1}: ${slide.name}`)}">
        <div class="brochure-presentation-slide-meta">
          <span class="num">${escapeHtml(String(index + 1).padStart(2, "0"))}</span>
          <span class="label">${escapeHtml(slide.name)}</span>
        </div>
        <iframe
          title="${escapeHtml(slide.name)}"
          srcdoc="${escapeHtml(slide.srcdoc)}"
          loading="lazy"
          scrolling="no"
        ></iframe>
      </section>
    `).join("");
    brochurePresentationSignature = signature;
  }
  updateBrochurePresentationHud();
  syncModalState();
}

function getBrochurePresentationSlides() {
  if (!elements.brochurePresentationMain) {
    return [];
  }
  return Array.from(elements.brochurePresentationMain.querySelectorAll(".brochure-presentation-slide"));
}

function updateBrochurePresentationHud() {
  const slides = getBrochurePresentationSlides();
  if (!elements.brochurePresentationHud || !slides.length) {
    return;
  }
  const current = Math.min(Math.max(brochurePresentationIndex + 1, 1), slides.length);
  elements.brochurePresentationHud.textContent = `${String(current).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}`;
}

function showBrochurePresentationHint() {
  if (!elements.brochurePresentationHint) {
    return;
  }
  elements.brochurePresentationHint.classList.remove("fade");
  if (brochurePresentationHintTimer) {
    window.clearTimeout(brochurePresentationHintTimer);
  }
  brochurePresentationHintTimer = window.setTimeout(() => {
    elements.brochurePresentationHint?.classList.add("fade");
  }, 3000);
}

function showBrochurePresentationHudBriefly() {
  if (!elements.brochurePresentationHud) {
    return;
  }
  elements.brochurePresentationHud.classList.remove("fade");
  if (brochurePresentationHudTimer) {
    window.clearTimeout(brochurePresentationHudTimer);
  }
  brochurePresentationHudTimer = window.setTimeout(() => {
    elements.brochurePresentationHud?.classList.add("fade");
  }, 1500);
}

function scaleBrochurePresentationIframe(slide) {
  const iframe = slide?.querySelector("iframe");
  if (!iframe) {
    return;
  }
  try {
    const doc = iframe.contentDocument;
    if (!doc || !doc.documentElement) {
      return;
    }
    const iframeWidthPx = iframe.getBoundingClientRect().width;
    const scale = iframeWidthPx / 1123;
    doc.documentElement.style.zoom = scale;
  } catch (error) {
    // Ignore iframe sizing failures.
  }
}

function unscaleBrochurePresentationIframe(slide) {
  const iframe = slide?.querySelector("iframe");
  if (!iframe) {
    return;
  }
  try {
    const doc = iframe.contentDocument;
    if (doc?.documentElement) {
      doc.documentElement.style.zoom = "";
    }
  } catch (error) {
    // Ignore iframe sizing failures.
  }
}

function setBrochurePresentationCurrent(index) {
  const slides = getBrochurePresentationSlides();
  if (!slides.length) {
    return;
  }

  if (index < 0) {
    index = 0;
  }
  if (index >= slides.length) {
    index = slides.length - 1;
  }

  if (slides[brochurePresentationIndex]) {
    unscaleBrochurePresentationIframe(slides[brochurePresentationIndex]);
  }
  brochurePresentationIndex = index;
  slides.forEach((slide, slideIndex) => {
    slide.classList.toggle("current", slideIndex === brochurePresentationIndex);
  });
  window.requestAnimationFrame(() => {
    scaleBrochurePresentationIframe(slides[brochurePresentationIndex]);
  });
  updateBrochurePresentationHud();
  showBrochurePresentationHudBriefly();
}

function isBrochurePresenting() {
  return elements.brochurePresentationBackdrop?.classList.contains("is-presenting");
}

function enterBrochurePresentation(startIndex = 0) {
  if (!elements.brochurePresentationBackdrop) {
    return;
  }
  elements.brochurePresentationBackdrop.classList.add("is-presenting");
  document.body.classList.add("brochure-presenting");
  document.documentElement.classList.add("brochure-presenting");
  setBrochurePresentationCurrent(startIndex);
  showBrochurePresentationHint();

  const fullscreenTarget = document.documentElement;
  const requestFullscreen = fullscreenTarget.requestFullscreen
    || fullscreenTarget.webkitRequestFullscreen
    || fullscreenTarget.msRequestFullscreen;
  if (requestFullscreen) {
    try {
      const result = requestFullscreen.call(fullscreenTarget);
      if (result?.catch) {
        result.catch(() => {});
      }
    } catch (error) {
      // Ignore fullscreen request failures.
    }
  }
}

async function ensureBrochureSlidesLoaded() {
  if (brochureSlidesLoading || brochureSlides.length) {
    return;
  }

  brochureSlidesLoading = true;
  brochureLoadError = "";
  renderBrochureBuilderPanel();

  try {
    const response = await window.fetch(BROCHURE_RESOURCE_PATH, { credentials: "same-origin" });
    if (!response.ok) {
      throw new Error("Could not load the hosted brochure file.");
    }
    const brochureHtml = await response.text();
    brochureSlides = parseBrochureSlides(brochureHtml);
    if (!brochureSlides.length) {
      throw new Error("No brochure slides were found in the hosted brochure.");
    }
    state.brochureBuilderSelectedIds = state.brochureBuilderSelectedIds.filter((id) => brochureSlides.some((slide) => slide.id === id));
    saveState();
  } catch (error) {
    brochureLoadError = error.message || "Could not load the brochure builder.";
  } finally {
    brochureSlidesLoading = false;
    renderBrochureBuilderPanel();
    renderBrochurePresentation();
  }
}

function parseBrochureSlides(brochureHtml) {
  const parser = new window.DOMParser();
  const documentNode = parser.parseFromString(brochureHtml, "text/html");
  return Array.from(documentNode.querySelectorAll("main .slide")).map((slide, index) => {
    const iframe = slide.querySelector("iframe");
    const rawLabel = slide.querySelector(".slide-meta .label")?.textContent?.trim()
      || slide.querySelector(".slide-meta")?.textContent?.trim()
      || `Slide ${index + 1}`;
    const numberMatch = rawLabel.match(/^(\d+)/);
    const number = numberMatch ? numberMatch[1].padStart(2, "0") : String(index + 1).padStart(2, "0");
    return {
      id: slide.id || `brochure-slide-${number}`,
      number,
      rawLabel,
      name: formatBrochureSlideName(rawLabel, number),
      srcdoc: iframe?.getAttribute("srcdoc") || "",
    };
  }).filter((slide) => slide.srcdoc);
}

function formatBrochureSlideName(rawLabel, fallbackNumber) {
  const cleaned = String(rawLabel || "")
    .replace(/^\s*\d+\s*-\s*/, "")
    .trim();
  if (!cleaned) {
    return `Slide ${fallbackNumber}`;
  }
  return cleaned
    .split(" - ")
    .map((segment) => segment
      .split(/\s+/)
      .map((word) => formatBrochureWord(word))
      .join(" "))
    .join(" · ");
}

function formatBrochureWord(word) {
  const compact = String(word || "").trim();
  if (!compact) {
    return "";
  }
  const normalized = compact.toLowerCase();
  const replacements = {
    md: "MD",
    ceo: "CEO",
    sebi: "SEBI",
    rbi: "RBI",
    csr: "CSR",
    llm: "LLM",
  };
  if (replacements[normalized]) {
    return replacements[normalized];
  }
  if (compact === "&") {
    return compact;
  }
  return capitalize(normalized);
}

function getBrochureSlideById(slideId) {
  return brochureSlides.find((slide) => slide.id === slideId) || null;
}

function getSelectedBrochureSlides() {
  return state.brochureBuilderSelectedIds
    .map((slideId) => getBrochureSlideById(slideId))
    .filter(Boolean);
}

function toggleBrochureSlideSelection(slideId, isSelected) {
  if (!slideId) {
    return;
  }

  const selectedIds = state.brochureBuilderSelectedIds.filter((id) => id !== slideId);
  if (isSelected) {
    selectedIds.push(slideId);
  }
  state.brochureBuilderSelectedIds = selectedIds;
  saveState();

  const selectedSlides = getSelectedBrochureSlides();
  if (!selectedSlides.length) {
    brochurePresentationIndex = 0;
  } else if (brochurePresentationIndex >= selectedSlides.length) {
    brochurePresentationIndex = selectedSlides.length - 1;
  }

  renderBrochureBuilderPanel();
  renderBrochurePresentation();
}

function hydrateBrochureFrames(container, slides) {
  if (!container) {
    return;
  }
  container.querySelectorAll("[data-brochure-preview-id]").forEach((frame) => {
    const slide = slides.find((item) => item.id === frame.dataset.brochurePreviewId);
    if (slide) {
      frame.srcdoc = slide.srcdoc;
    }
  });
}

function printSelectedBrochureSlides() {
  const selectedSlides = getSelectedBrochureSlides();
  if (!selectedSlides.length) {
    showToast("Select at least one slide first.");
    return;
  }

  const printWindow = window.open("", "_blank");
  if (!printWindow) {
    showToast("Allow pop-ups to export the brochure.");
    return;
  }

  const slidesMarkup = selectedSlides.map((slide, index) => `
    <section class="print-slide">
      <iframe title="${escapeHtml(slide.name)}" srcdoc="${escapeHtml(slide.srcdoc)}"></iframe>
    </section>
  `).join("");

  printWindow.document.open();
  printWindow.document.write(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Acuité brochure export</title>
  <style>
    @page { size: A4 landscape; margin: 0; }
    * { box-sizing: border-box; }
    html, body {
      margin: 0;
      padding: 0;
      background: #ffffff;
      font-family: Helvetica, Arial, sans-serif;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .print-slide {
      width: 297mm;
      height: 210mm;
      page-break-after: always;
      break-after: page;
      overflow: hidden;
    }
    .print-slide:last-child {
      page-break-after: auto;
      break-after: auto;
    }
    iframe {
      width: 297mm;
      height: 210mm;
      border: 0;
      display: block;
      margin: 0;
      background: #ffffff;
    }
  </style>
</head>
<body>
  ${slidesMarkup}
  <script>
    window.addEventListener("load", function () {
      window.setTimeout(function () {
        window.focus();
        window.print();
      }, 700);
    });
    window.onafterprint = function () {
      window.close();
    };
  </script>
</body>
</html>`);
  printWindow.document.close();
  showToast("Print dialog opened. Save the PDF on your machine.");
}

function openBrochurePresentation() {
  const selectedSlides = getSelectedBrochureSlides();
  if (!selectedSlides.length) {
    showToast("Select at least one slide first.");
    return;
  }

  brochurePresentationOpen = true;
  brochurePresentationIndex = Math.min(brochurePresentationIndex, selectedSlides.length - 1);
  renderBrochurePresentation();
  enterBrochurePresentation(Math.max(brochurePresentationIndex, 0));
}

function closeBrochurePresentation(options = {}) {
  const { skipFullscreenExit = false } = options;
  brochurePresentationOpen = false;
  brochurePresentationSignature = "";
  brochurePresentationIndex = 0;
  if (brochurePresentationHudTimer) {
    window.clearTimeout(brochurePresentationHudTimer);
    brochurePresentationHudTimer = null;
  }
  if (brochurePresentationHintTimer) {
    window.clearTimeout(brochurePresentationHintTimer);
    brochurePresentationHintTimer = null;
  }
  elements.brochurePresentationBackdrop?.classList.remove("is-presenting");
  elements.brochurePresentationHud?.classList.remove("fade");
  elements.brochurePresentationHint?.classList.remove("fade");
  document.body.classList.remove("brochure-presenting");
  document.documentElement.classList.remove("brochure-presenting");
  if (elements.brochurePresentationMain) {
    getBrochurePresentationSlides().forEach((slide) => {
      slide.classList.remove("current");
      unscaleBrochurePresentationIframe(slide);
    });
    elements.brochurePresentationMain.innerHTML = "";
  }
  renderBrochurePresentation();
  if (!skipFullscreenExit && document.fullscreenElement) {
    const exitFullscreen = document.exitFullscreen || document.webkitExitFullscreen || document.msExitFullscreen;
    if (exitFullscreen) {
      try {
        const result = exitFullscreen.call(document);
        if (result?.catch) {
          result.catch(() => {});
        }
      } catch (error) {
        // Ignore fullscreen exit failures.
      }
    }
  }
}

function moveBrochurePresentation(direction) {
  const slides = getBrochurePresentationSlides();
  if (!slides.length) {
    return;
  }
  setBrochurePresentationCurrent((brochurePresentationIndex + direction + slides.length) % slides.length);
}

function syncModalState() {
  const anyModalOpen = [
    elements.commentsModalBackdrop,
    elements.announcementReminderBackdrop,
    elements.brochurePresentationBackdrop,
  ].some((modal) => modal && !modal.hidden);
  document.body.classList.toggle("modal-open", anyModalOpen);
}

function getCurrentLocalDateStamp() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function getAnnouncementReminderUserKey() {
  return String(appData.currentUser?.id || appData.currentUser?.email || "").trim();
}

function readAnnouncementReminderState() {
  try {
    const raw = window.localStorage.getItem(ANNOUNCEMENT_REMINDER_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch (error) {
    return {};
  }
}

function saveAnnouncementReminderState(stateSnapshot) {
  try {
    window.localStorage.setItem(ANNOUNCEMENT_REMINDER_KEY, JSON.stringify(stateSnapshot));
  } catch (error) {
    return;
  }
}

function closeAnnouncementReminder() {
  if (!elements.announcementReminderBackdrop) {
    return;
  }
  elements.announcementReminderBackdrop.hidden = true;
  syncModalState();
}

function openAnnouncementReminder() {
  if (!elements.announcementReminderBackdrop) {
    return;
  }
  elements.announcementReminderBackdrop.hidden = false;
  syncModalState();
}

function showAnnouncementReminderIfNeeded() {
  const userKey = getAnnouncementReminderUserKey();
  if (!userKey) {
    return;
  }
  const today = getCurrentLocalDateStamp();
  const saved = readAnnouncementReminderState();
  if (saved[userKey] === today) {
    return;
  }
  saved[userKey] = today;
  saveAnnouncementReminderState(saved);
  openAnnouncementReminder();
}

function renderCeoDeskMessage() {
  const dateEl = document.getElementById("ceo-desk-message-date");
  const titleEl = document.getElementById("ceo-desk-message-title");
  const copyEl = document.getElementById("ceo-desk-copy");
  const actionsEl = document.querySelector(".ceo-desk-actions");
  const archiveEl = document.getElementById("ceo-desk-archive-list");
  const form = document.getElementById("ceo-desk-post-form");
  const message = getCurrentCeoDeskMessage();
  const viewingArchive = Boolean(selectedCeoDeskArchiveKey);

  if (dateEl) {
    dateEl.textContent = message.date;
  }
  if (titleEl) {
    titleEl.textContent = message.title;
  }
  if (copyEl) {
    const bodyParts = Array.isArray(message.body) ? message.body : DEFAULT_CEO_DESK_MESSAGE.body;
    copyEl.innerHTML = bodyParts
      .map((paragraph) => `<p>${escapeHtml(String(paragraph || "")).replace(/\n/g, "<br>")}</p>`)
      .join("");
  }
  if (actionsEl) {
    actionsEl.innerHTML = `
      ${
        viewingArchive
          ? '<button type="button" class="btn-ghost ceo-desk-return-btn" data-action="return-ceo-current-message">Back to current message</button>'
          : ""
      }
      <button type="button" class="ceo-desk-like-btn" id="ceo-desk-like-btn"></button>
    `;
  }
  if (archiveEl) {
    const archiveItems = getCeoDeskArchiveItems();
    archiveEl.innerHTML = archiveItems.length
      ? archiveItems.map((item) => `
          <button
            type="button"
            class="ceo-desk-archive-link ${selectedCeoDeskArchiveKey === item.archiveKey ? "active" : ""}"
            data-action="open-ceo-archive-message"
            data-archive-key="${escapeHtml(item.archiveKey)}"
          >
            <span>${escapeHtml(
              [item.datePosted, item.headline].filter(Boolean).join(" | "),
            )}</span>
          </button>
        `).join("")
      : '<div class="mini-item-meta">No previous messages yet.</div>';
  }
  if (form && currentUserCanPostCeoMessage() && !form.dataset.seeded) {
    form.elements.headline.value = "";
    form.elements.body.value = "";
    form.dataset.seeded = "true";
  }
}

function scrollCeoDeskMessageIntoView() {
  const container = document.querySelector(".ceo-desk-editorial");
  if (!container) {
    return;
  }
  window.requestAnimationFrame(() => {
    container.scrollIntoView({ behavior: "smooth", block: "start" });
  });
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

function currentUserCanPostCeoMessage() {
  return currentUserCanAdministerConnect();
}

function renderPanels() {
  const canAdminister = currentUserCanAdministerConnect();
  if (state.activeTab === "clubs-learning") {
    state.activeTab = "library";
    saveState();
  }
  if (!ENABLED_TABS.has(state.activeTab)) {
    state.activeTab = "home";
    saveState();
  }
  const activeSidebarTab = ["battleship", "quiz"].includes(state.activeTab) ? "playtime" : state.activeTab;
  if (state.activeTab === "admin") {
    state.activeTab = "home";
    saveState();
  }
  applyTheme();
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
  const ceoPostForm = document.getElementById("ceo-desk-post-form");
  if (ceoPostForm) {
    ceoPostForm.hidden = !currentUserCanPostCeoMessage();
  }
  document.querySelectorAll(".panel").forEach((panel) => {
    panel.classList.toggle("active", panel.id === `panel-${state.activeTab}`);
  });
  document.querySelectorAll(".sidebar-left .tab").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.switchTab === activeSidebarTab);
  });
  document.querySelectorAll(".topnav-right [data-switch-tab]").forEach((button) => {
    button.classList.toggle("active", button.dataset.switchTab === state.activeTab);
  });
}

function renderProfile() {
  const canAdminister = currentUserCanAdministerConnect();
  const totalComments = appData.myPosts.reduce(
    (sum, post) => sum + Number(post.commentCount || 0),
    0,
  );
  const availableCoins = Number(appData.storeBalance.available_points || 0);
  const totalLikes = appData.myPosts.reduce(
    (sum, post) => sum + Number(post.reactionCount || 0),
    0,
  );

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
  elements.profileKudos.textContent = String(totalComments);
  elements.profileClubs.textContent = String(availableCoins);
  elements.profilePitches.textContent = String(totalLikes);
  if (elements.profileMenu) {
    elements.profileMenu.hidden = !profileMenuOpen;
  }
}

function renderProfileBuilder() {
  if (!elements.profileBuilderForm) {
    return;
  }

  elements.profileBuilderForm.classList.toggle("is-disabled", Boolean(profileBuilderLoadError));
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

  if (elements.profileHobbiesInput) {
    const hobbyOptions = appData.communityClubs.length
      ? appData.communityClubs.map((club) => club.label)
      : [];
    elements.profileHobbiesInput.innerHTML = hobbyOptions.length
      ? hobbyOptions.map((hobby) => `
          <button
            type="button"
            class="profile-skill-chip ${profileBuilderDraft.hobbies.includes(hobby) ? "active" : ""}"
            data-action="toggle-profile-hobby"
            data-hobby="${escapeHtml(hobby)}"
          >
            ${escapeHtml(hobby)}
          </button>
        `).join("")
      : `<div class="mini-item-meta">Community clubs are loading...</div>`;
  }

  if (elements.profileBuilderStatus) {
    elements.profileBuilderStatus.textContent = profileBuilderLoadError
      ? profileBuilderLoadError
      : "Add up to 2 photos, choose up to 3 skills and 3 hobbies, and tell colleagues what you enjoy.";
  }
}

function findLivePostById(postId) {
  const targetId = Number(postId || 0);
  if (!targetId) {
    return null;
  }
  const allPosts = [
    ...appData.bulletinPosts,
    ...appData.myPosts,
    ...Object.values(appData.communityPostsByClub).flat(),
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
  syncModalState();

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
  syncModalState();
}

function renderCommentsModal() {
  if (!elements.commentsModalBackdrop || !elements.commentsModalList || !elements.commentsModalMeta) {
    return;
  }

  if (!activeCommentsPostId) {
    elements.commentsModalBackdrop.hidden = true;
    syncModalState();
    return;
  }

  const post = findLivePostById(activeCommentsPostId);
  elements.commentsModalBackdrop.hidden = false;
  syncModalState();
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
    elements.myPostsForm,
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

  const publishedPost = getHomeAnnouncementPostForTag(state.homeAnnouncementFilter);
  const announcement = publishedPost
    ? mapHomeAnnouncementPost(publishedPost)
    : (HOME_ANNOUNCEMENTS.find((item) => item.tag === state.homeAnnouncementFilter) || null);
  renderHomeAnnouncementFilters();
  renderHomeAnnouncementAdminForm();
  if (!announcement) {
    container.innerHTML = `
      <div class="announcement-empty-state">
        <p class="widget-kicker">Announcements</p>
        <h2>No announcement published under this tag yet.</h2>
        <p>Select another capsule button or publish a real announcement under this tag.</p>
      </div>
    `;
    return;
  }
  const liked = announcement.isLive
    ? Boolean(announcement.currentUserHasReacted)
    : state.likedPostIds.includes(announcement.id);
  const totalLikes = announcement.isLive
    ? Number(announcement.baseMetrics?.likes || 0)
    : Number(announcement.baseMetrics?.likes || 0) + (liked ? 1 : 0);
  const likeAction = announcement.isLive ? "toggle-live-reaction" : "toggle-like";
  const likeTarget = announcement.isLive ? announcement.sourceId : announcement.id;
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
      <form class="announcement-feedback-form" id="home-announcement-feedback-form">
        <label class="announcement-feedback-label" for="home-announcement-feedback-input">Post Your Idea, Suggestion, Question</label>
        <textarea
          id="home-announcement-feedback-input"
          name="body"
          class="announcement-feedback-input"
          rows="5"
          placeholder="Write one clear point for leadership here."
        ></textarea>
        <div class="announcement-feedback-actions">
          <button type="submit" class="announcement-feedback-submit">Submit to Admin</button>
          <span class="announcement-feedback-reward">Earn 1000 Acuite Coins</span>
        </div>
      </form>
      <div class="announcement-like-row">
        <button type="button" class="announcement-like-btn ${liked ? "liked" : ""}" data-action="${likeAction}" data-id="${escapeHtml(String(likeTarget))}">
          ${liked ? "Liked" : "Like"}
        </button>
        <span class="announcement-like-count">${escapeHtml(String(totalLikes))} like${totalLikes === 1 ? "" : "s"}</span>
      </div>
    </div>
  `;
}

function renderHomeAnnouncementFilters() {
  const row = document.getElementById("home-announcement-filters");
  if (!row) {
    return;
  }
  row.querySelectorAll("[data-action='set-home-announcement-filter']").forEach((button) => {
    button.classList.toggle("active", button.dataset.filter === state.homeAnnouncementFilter);
  });
}

function renderHomeAnnouncementAdminForm() {
  const form = document.getElementById("home-announcement-admin-form");
  const title = document.getElementById("home-announcement-admin-title");
  if (!form || !title) {
    return;
  }
  form.hidden = !currentUserCanAdministerConnect();
  title.textContent = `Publish under ${getSelectedHomeAnnouncementFilterLabel()}`;
  syncHomeAnnouncementAdminForm(form);
}

async function submitHomeAnnouncementFeedback(form) {
  if (!currentUserCanCreatePosts()) {
    showToast("Your posting access is currently disabled.");
    return;
  }

  const announcement = getCurrentHomeAnnouncement();
  if (!announcement) {
    showToast("There is no live announcement under this tag right now.");
    return;
  }

  const formData = new FormData(form);
  const body = String(formData.get("body") || "").trim();
  if (!body) {
    showToast("Write your idea, suggestion, or question first.");
    return;
  }

  try {
    await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
      method: "POST",
      body: {
        title: "Town hall response",
        body,
        module: FEED_MODULE_EMPLOYEE_POSTS,
        kind: "update",
        topic: "employee_submission",
        metadata: {
          bulletin_category: "employee_posts",
          submission_key: "town_hall_response",
          submission_label: "Town hall response",
          bulletin_meta_lines: [announcement.dateLabel],
          town_hall_response: true,
        },
      },
    });
    form.reset();
    showToast("Your note has been sent for admin review.");
  } catch (error) {
    showToast(error.message || "Could not send your note to admin.");
  }
}

async function submitHomeAnnouncementAdminPost(form) {
  if (!currentUserCanAdministerConnect()) {
    showToast("Admin access is required to publish announcements here.");
    return;
  }

  const formData = new FormData(form);
  const announcementType = String(formData.get("announcement_type") || "other").trim();
  let title = "";
  let body = "";
  let metaLines = [];
  const metadata = {
    bulletin_category: "announcements",
    bulletin_channel: "announcements",
    home_announcement_tag: state.homeAnnouncementFilter,
    home_announcement_type: announcementType,
  };

  if (announcementType === "town_hall") {
    const townHallDate = String(formData.get("town_hall_date") || "").trim();
    const townHallTime = String(formData.get("town_hall_time") || "").trim();
    const townHallMode = String(formData.get("town_hall_mode") || "").trim();
    const townHallVenue = String(formData.get("town_hall_venue") || "").trim();
    if (!townHallDate || !townHallTime || !townHallMode || !townHallVenue) {
      showToast("Add the date, time, mode, and venue before publishing a town hall.");
      return;
    }
    title = TOWN_HALL_GENERIC_CONTENT.title;
    body = TOWN_HALL_GENERIC_CONTENT.summary;
    metaLines = [formatAnnouncementLongDate(townHallDate)];
    metadata.home_announcement_town_hall = {
      date: townHallDate,
      time: townHallTime,
      mode: townHallMode,
      venue: normalizeTownHallVenueLabel(townHallVenue),
    };
  } else {
    title = String(formData.get("title") || "").trim();
    const metaLine = String(formData.get("meta_line") || "").trim();
    body = String(formData.get("body") || "").trim();
    if (!title || !body) {
      showToast("Add both a headline and body before publishing.");
      return;
    }
    metadata.home_announcement_town_hall = null;
    metaLines = metaLine ? [metaLine] : [];
  }

  metadata.bulletin_meta_lines = metaLines;

  try {
    await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
      method: "POST",
      body: {
        title,
        body,
        kind: "announcement",
        module: FEED_MODULE_BULLETIN,
        topic: "announcements",
        post_as_company: true,
        allow_comments: true,
        metadata,
      },
    });
    form.reset();
    syncHomeAnnouncementAdminForm(form);
    await loadHomeAnnouncementPosts();
    renderHomeAnnouncement();
    showToast(announcementType === "town_hall"
      ? "Town hall announcement published."
      : `${getSelectedHomeAnnouncementFilterLabel()} announcement published.`);
  } catch (error) {
    showToast(error.message || "Could not publish the announcement.");
  }
}

function prefillCeoDeskComment(message) {
  const input = document.getElementById("ceo-desk-comment-input");
  const form = document.getElementById("ceo-desk-comment-form");
  const selectedButton = document.activeElement?.closest?.(".ceo-desk-link[data-request-key]");
  if (!input) {
    return;
  }
  if (form && selectedButton) {
    form.dataset.requestKey = selectedButton.dataset.requestKey || "comment";
    form.dataset.requestLabel = selectedButton.dataset.requestLabel || "MD & CEO desk comment";
  }
  input.value = String(message || "").trim();
  input.focus();
  input.setSelectionRange(input.value.length, input.value.length);
}

async function submitCeoDeskComment(form) {
  if (!currentUserCanCreatePosts()) {
    showToast("Your posting access is currently disabled.");
    return;
  }

  const formData = new FormData(form);
  const body = String(formData.get("body") || "").trim();
  if (!body) {
    showToast("Write your comment first.");
    return;
  }

  const input = document.getElementById("ceo-desk-comment-input");
  const requestKey = form.dataset.requestKey || "comment";
  const requestLabel = form.dataset.requestLabel || "MD & CEO desk comment";
  const submissionKey = requestKey === "comment" ? "ceo_desk_comment" : `ceo_request_${requestKey}`;

  try {
    await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
      method: "POST",
      body: {
        title: requestLabel,
        body,
        module: FEED_MODULE_EMPLOYEE_POSTS,
        kind: "update",
        topic: "employee_submission",
        metadata: {
          bulletin_category: "employee_posts",
          submission_key: submissionKey,
          submission_label: "MD & CEO request",
          bulletin_meta_lines: ["MD & CEO's Desk"],
          ceo_desk_request: true,
          ceo_desk_request_key: requestKey,
          ceo_desk_request_label: requestLabel,
        },
      },
    });
    form.reset();
    form.dataset.requestKey = "comment";
    form.dataset.requestLabel = "MD & CEO desk comment";
    if (input) {
      input.value = "";
    }
    showToast("Your comment has been sent to admin.");
  } catch (error) {
    showToast(error.message || "Could not send your comment.");
  }
}

async function submitCeoDeskPost(form) {
  if (!currentUserCanPostCeoMessage()) {
    showToast("This message form is available only to Connect admins.");
    return;
  }

  const formData = new FormData(form);
  const headline = String(formData.get("headline") || "").trim();
  const body = String(formData.get("body") || "").trim();
  const messageDate = formatCeoDeskPostedDate(new Date().toISOString());

  if (!headline || !body) {
    showToast("Complete the headline and body first.");
    return;
  }

  try {
    await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
      method: "POST",
      body: {
        title: headline,
        body,
        kind: "announcement",
        module: FEED_MODULE_BULLETIN,
        topic: "announcements",
        post_as_company: true,
        allow_comments: false,
        metadata: {
          bulletin_category: "announcements",
          bulletin_channel: "ceo_desk",
          bulletin_template: "ceo_editorial",
          bulletin_meta_lines: [messageDate],
        },
      },
    });
    await loadCeoDeskPosts();
    selectedCeoDeskArchiveKey = "";
    renderCeoDeskMessage();
    renderCeoDeskLikeButton();
    form.reset();
    form.dataset.seeded = "true";
    showToast("The MD & CEO message is now live in the main section and the previous one has moved to the archive.");
  } catch (error) {
    showToast(error.message || "Could not publish the MD & CEO message.");
  }
}

function renderLearningPanel() {
  renderLearningSummary();
  renderLearningBooks();
}

function renderStorePanel() {
  renderStoreSummary();
  renderStoreCatalog();
  renderStoreBalanceCard();
  renderStoreRedemptionsCard();
  renderStorePolicyCard();
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
  const container = document.getElementById("store-summary-grid");
  if (!container) {
    return;
  }
  const items = getFilteredStoreItems();
  const availableItems = appData.storeItems.filter((item) => item.available_units > 0).length;

  container.innerHTML = [
    {
      kicker: "Balance",
      title: `${appData.storeBalance.available_points || 0} coins`,
      copy: "Acuite Coins available right now for Brand Store redemption.",
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
  const meta = document.getElementById("store-results-meta");
  if (!container || !meta) {
    return;
  }
  if (storeLoadError) {
    meta.textContent = "Store load issue";
    container.innerHTML = `<div class="empty-state">${escapeHtml(storeLoadError)}</div>`;
    return;
  }

  const items = getFilteredStoreItems();
  meta.textContent = appData.storeItems.length
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
  const container = document.getElementById("store-balance-card");
  if (!container) {
    return;
  }
  container.innerHTML = `
    <p class="widget-kicker">My Acuite Coins</p>
    <h3>${escapeHtml(String(appData.storeBalance.available_points || 0))} available</h3>
    <ul class="simple-list">
      <li>Earned: ${escapeHtml(String(appData.storeBalance.earned_points || 0))} coins</li>
      <li>Locked in requests: ${escapeHtml(String(appData.storeBalance.locked_points || 0))} coins</li>
      <li>Encashed: ${escapeHtml(String(appData.storeBalance.spent_points || 0))} coins</li>
      <li>Expired: ${escapeHtml(String(appData.storeBalance.expired_points || 0))} coins</li>
    </ul>
    <div class="mini-item-meta">Unused balance expires on 31 March or on the employee’s day of exit.</div>
  `;
}

function renderStoreRedemptionsCard() {
  const container = document.getElementById("store-redemptions-card");
  if (!container) {
    return;
  }
  container.innerHTML = `
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
  const container = document.getElementById("store-policy-card");
  if (!container) {
    return;
  }
  const register = Array.isArray(appData.storeBalance.register) ? appData.storeBalance.register.slice(0, 5) : [];
  container.innerHTML = `
    <p class="widget-kicker">Coin register</p>
    <h3>Recent coin activity</h3>
    ${
      register.length
        ? `<ul class="mini-list">
            ${register.map((entry) => `
              <li>
                <div>
                  <div class="mini-item-title">${escapeHtml(entry.label || "Acuite Coins activity")}</div>
                  <div class="mini-item-meta">${escapeHtml(entry.summary || "")}</div>
                </div>
                <div class="mini-item-time ${entry.amount < 0 ? "negative-balance" : ""}">${escapeHtml(`${entry.amount > 0 ? "+" : ""}${entry.amount}c`)}</div>
              </li>
            `).join("")}
          </ul>`
        : `<div class="empty-state">Your Acuite Coin register will appear here after live activity begins.</div>`
    }
  `;
}

function renderStoreItemCard(item) {
  const canAdminister = currentUserCanAdministerConnect();
  const accent = item.accent_hex || "#e8722a";
  const activeRedemption = appData.storeRedemptions.find((redemption) => {
    return redemption.item.id === item.id
      && ["requested", "approved", "fulfilled"].includes(redemption.status);
  });
  const availablePoints = Number(appData.storeBalance.available_points || 0);
  const coinCost = Number(item.coin_cost || item.point_cost || 0);
  const missingPoints = Math.max(coinCost - availablePoints, 0);
  const outOfStock = item.available_units <= 0;
  const canRedeem = !activeRedemption && !outOfStock && availablePoints >= coinCost;
  let actionLabel = "Buy with Acuite Coins";

  if (activeRedemption) {
    actionLabel = capitalize(activeRedemption.status);
  } else if (outOfStock) {
    actionLabel = "Out of stock";
  } else if (missingPoints > 0) {
    actionLabel = `Need ${missingPoints} coins`;
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
          <div class="store-item-head-actions">
            <div class="store-item-cost">${escapeHtml(String(coinCost))} coins</div>
            ${
              canAdminister
                ? `<button
                    type="button"
                    class="btn-link post-delete-btn"
                    data-action="delete-store-item"
                    data-id="${item.id}"
                  >
                    Delete
                  </button>`
                : ""
            }
          </div>
        </div>
        <p>${escapeHtml(item.description || "Admin-managed branded merchandise available for Acuite Coin redemption inside Connect.")}</p>
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
            : escapeHtml(`Use ${coinCost} Acuite Coins to request this item`)}
        </span>
        <div class="store-item-actions">
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
      </div>
    </article>
  `;
}

async function deleteStoreItem(itemId) {
  if (!itemId || !currentUserCanAdministerConnect()) {
    return;
  }

  try {
    await window.AcuiteConnectAuth.apiRequest(`/api/store/items/${itemId}/`, {
      method: "DELETE",
    });
    await loadStoreData();
    renderStorePanel();
    showToast("Brand Store item removed.");
  } catch (error) {
    showToast(error.message || "Could not remove the Brand Store item.");
  }
}

function renderBulletinPanel() {
  const container = document.getElementById("bulletin-feed");
  if (!container) {
    return;
  }

  if (bulletinLoadError) {
    container.innerHTML = `<div class="empty-state">${escapeHtml(bulletinLoadError)}</div>`;
    return;
  }

  const posts = getVisibleBulletinBoardPosts();
  if (!posts.length) {
    container.innerHTML = `
      <div class="empty-state">
        No company bulletin posts from the last 30 days are visible right now.
      </div>
    `;
    return;
  }

  container.innerHTML = posts.map(renderBulletinPostCard).join("");
}

function renderMyPostsPanel() {
  if (elements.myPostsTypeSelect && elements.myPostsTypeSelect.options.length <= 1) {
    elements.myPostsTypeSelect.innerHTML = `
      <option value="">Choose one</option>
      ${MY_POST_TYPES.map((item) => `<option value="${escapeHtml(item.key)}">${escapeHtml(item.label)}</option>`).join("")}
    `;
  }

  syncMyPostsComposer();

  if (!elements.myPostsList || !elements.myPostsResultsMeta) {
    return;
  }

  if (myPostsLoadError) {
    elements.myPostsResultsMeta.textContent = "My Posts issue";
    elements.myPostsList.innerHTML = `<div class="empty-state">${escapeHtml(myPostsLoadError)}</div>`;
    return;
  }

  if (!appData.myPosts.length) {
    elements.myPostsResultsMeta.textContent = "No submissions yet";
    elements.myPostsList.innerHTML = '<div class="empty-state">Your submitted posts will appear here after your first draft is sent for review.</div>';
    return;
  }

  elements.myPostsResultsMeta.textContent = `${appData.myPosts.length} submission${appData.myPosts.length === 1 ? "" : "s"}`;
  elements.myPostsList.innerHTML = appData.myPosts.map((post) => `
    <article class="summary-card foundation-card">
      <strong>${escapeHtml(post.title)}</strong>
      <span class="mini-chip ${post.moderationStatus === "published" ? "success" : ""}">
        ${escapeHtml(post.moderationLabel)}
      </span>
      <p>${escapeHtml(post.submissionLabel)}</p>
      ${post.metaLine ? `<div class="mini-item-meta">${escapeHtml(post.metaLine)}</div>` : ""}
      <div class="mini-item-meta">${escapeHtml(formatRelativeTime(post.publishedAt || post.createdAt))}</div>
    </article>
  `).join("");
}

function renderCommunityPanel() {
  if (!elements.communityGrid || !elements.communityResultsMeta || !elements.communityWorkspaceBody) {
    return;
  }

  if (state.activeTab === "community" && !communityLoading && !communityLoadError && !appData.communityClubs.length) {
    void loadCommunityData();
  }

  if (communityLoadError) {
    elements.communityResultsMeta.textContent = "Community issue";
    elements.communityGrid.innerHTML = `<div class="empty-state">${escapeHtml(communityLoadError)}</div>`;
    elements.communityWorkspaceBody.innerHTML = `<div class="empty-state">${escapeHtml(communityLoadError)}</div>`;
    return;
  }

  if (communityLoading && !appData.communityClubs.length) {
    elements.communityResultsMeta.textContent = "Loading communities...";
    elements.communityGrid.innerHTML = '<div class="empty-state">Loading communities...</div>';
    elements.communityWorkspaceBody.innerHTML = '<div class="empty-state">Loading communities...</div>';
    return;
  }

  if (!appData.communityClubs.length) {
    elements.communityResultsMeta.textContent = "No communities available";
    elements.communityGrid.innerHTML = '<div class="empty-state">No communities have been published yet.</div>';
    elements.communityWorkspaceBody.innerHTML = '<div class="empty-state">No community clubs are available yet.</div>';
    return;
  }

  syncActiveCommunityClub();
  const joinedCount = appData.communityClubs.filter((club) => club.joined).length;
  elements.communityResultsMeta.textContent = `${appData.communityClubs.length} communities | ${joinedCount} joined`;
  elements.communityWorkspaceBody.innerHTML = renderCommunityWorkspace(getActiveCommunityClub());
  elements.communityGrid.innerHTML = appData.communityClubs.map((club) => `
    <article class="section-card club-card ${state.communityClubKey === club.key ? "active" : ""}">
      <div class="club-banner ${communityGradientClass(club.key)}">
        <div class="club-emoji">${escapeHtml(COMMUNITY_CLUB_EMOJIS[club.key] || "✨")}</div>
      </div>
      <div class="club-card-body">
        <h3>${escapeHtml(club.label)}</h3>
        <p>${escapeHtml(club.description || "Select this club in My Profile hobbies to participate with colleagues.")}</p>
        <div class="mini-item-meta">
          ${
            club.club_admin?.name
              ? `Club Admin: ${escapeHtml([club.club_admin.name, club.club_admin.title].filter(Boolean).join(" | "))}`
              : "Club Admin will be assigned to the first employee who selects this club in My Profile."
          }
        </div>
        <div class="club-members">
          <span class="count">${escapeHtml(String(club.member_count || 0))} member${Number(club.member_count || 0) === 1 ? "" : "s"}</span>
          <div class="community-club-actions">
            <button
              type="button"
              class="btn-link"
              data-action="select-community-club"
              data-club-key="${escapeHtml(club.key)}"
            >
              Open club
            </button>
            ${club.joined ? '<span class="mini-chip success">Joined</span>' : ""}
          </div>
        </div>
      </div>
    </article>
  `).join("");

  const activeClub = getActiveCommunityClub();
  if (activeClub?.joined && !Array.isArray(appData.communityPostsByClub[activeClub.key]) && !communityPostsErrorByClub[activeClub.key]) {
    void loadCommunityPosts(activeClub.key);
  }
}

function communityGradientClass(clubKey) {
  const groups = {
    reading_club: "club-banner-sun",
    movie_club: "club-banner-ember",
    travel_club: "club-banner-cool",
    entertainment_club: "club-banner-fire",
    quiz_club: "club-banner-leaf",
    debate_club: "club-banner-sun",
    technology_club: "club-banner-cool",
    photography_club: "club-banner-ember",
    cricket_club: "club-banner-leaf",
    football_club: "club-banner-cool",
    charity_club: "club-banner-fire",
    health_club: "club-banner-leaf",
  };
  return groups[clubKey] || "club-banner-sun";
}

function renderCommunityWorkspace(club) {
  if (!club) {
    return '<div class="empty-state">Choose a club to start exploring the community space.</div>';
  }

  const feedError = communityPostsErrorByClub[club.key] || "";
  const feedLoading = communityPostsLoadingKey === club.key && !Array.isArray(appData.communityPostsByClub[club.key]);
  const posts = Array.isArray(appData.communityPostsByClub[club.key]) ? sortBulletinPostsNewestFirst(appData.communityPostsByClub[club.key]) : [];
  const isSubmitting = communityPostsSubmittingKey === club.key;
  const form = club.form || {};
  const clubAdminLine = club.club_admin?.name
    ? [club.club_admin.name, club.club_admin.title, club.club_admin.location].filter(Boolean).join(" | ")
    : "Will be assigned automatically when the first employee selects this club in My Profile.";

  if (!club.joined) {
    return `
      <div class="community-workspace-head">
        <div>
          <p class="widget-kicker">Club space</p>
          <h2>${escapeHtml(club.label)}</h2>
          <div class="mini-item-meta">Club Admin: ${escapeHtml(clubAdminLine)}</div>
        </div>
        <div class="community-workspace-stats">
          <span class="mini-chip">${escapeHtml(String(club.member_count || 0))} members</span>
        </div>
      </div>
      <div class="empty-state">To join ${escapeHtml(club.label)}, open My Profile and select it under Hobbies. Once selected there, this club will show as Joined here.</div>
    `;
  }

  return `
    <div class="community-workspace-head">
      <div>
        <p class="widget-kicker">Club space</p>
        <h2>${escapeHtml(club.label)}</h2>
        <div class="mini-item-meta">
          Club Admin: ${escapeHtml(clubAdminLine)}
          ${club.viewer_is_admin ? " | You are the Club Admin." : ""}
        </div>
      </div>
      <div class="community-workspace-stats">
        <span class="mini-chip">${escapeHtml(String(club.member_count || 0))} members</span>
      </div>
    </div>
    <div class="community-workspace-grid">
      <section class="section-card community-composer-card">
        <div class="section-card-head">
          <div>
            <p class="widget-kicker">Post an update</p>
            <h3>${escapeHtml(club.label)} update form</h3>
            <div class="mini-item-meta">Posts published here are visible only to members of this club.</div>
          </div>
        </div>
        <form id="community-post-form" class="story-form" data-club-key="${escapeHtml(club.key)}">
          <label class="field">
            <span>${escapeHtml(form.primary_field_label || "Title")}</span>
            <input type="${escapeHtml(form.primary_field_type || "text")}" name="primary_value" placeholder="${escapeHtml(form.primary_field_label || "Enter the main detail")}" required>
          </label>
          <label class="field">
            <span>${escapeHtml(form.headline_label || "Headline")}</span>
            <input type="text" name="headline" placeholder="Write a short headline" required>
          </label>
          <label class="field">
            <span>${escapeHtml(form.body_label || "Body")}</span>
            <textarea name="body" rows="4" placeholder="Write the main update clearly." required></textarea>
          </label>
          <label class="field">
            <span>${escapeHtml(form.extra_field_label || "Additional detail")}</span>
            ${
              form.extra_field_type === "textarea"
                ? `<textarea name="extra_value" rows="4" placeholder="${escapeHtml(form.extra_field_label || "Add one more detail")}" required></textarea>`
                : `<input type="${escapeHtml(form.extra_field_type === "datetime" ? "datetime-local" : (form.extra_field_type || "text"))}" name="extra_value" placeholder="${escapeHtml(form.extra_field_label || "Add one more detail")}" required>`
            }
          </label>
          <div class="form-actions">
            <p class="mini-item-meta">Members can like and comment on club posts after they are published.</p>
            <button type="submit" class="btn-warm" ${isSubmitting ? "disabled" : ""}>${isSubmitting ? "Posting..." : "Post update"}</button>
          </div>
        </form>
      </section>
      <section class="section-card community-feed-shell">
        <div class="section-card-head">
          <div>
            <p class="widget-kicker">Club feed</p>
            <h3>${escapeHtml(club.label)} posts</h3>
            <div class="mini-item-meta">Only club members can view, like, and comment here.</div>
          </div>
        </div>
        <div class="community-feed">
          ${
            feedError
              ? `<div class="empty-state">${escapeHtml(feedError)}</div>`
              : feedLoading
                ? '<div class="empty-state">Loading club posts...</div>'
                : posts.length
                  ? posts.map(renderCommunityPostCard).join("")
                  : '<div class="empty-state">No club posts yet. Use the form to publish the first one.</div>'
          }
        </div>
      </section>
    </div>
  `;
}

function renderCommunityPostCard(post) {
  return `
    <article class="card community-post-card" id="${post.id}">
      <div class="card-header">
        <div class="card-avatar" style="background:${gradientValue(post.avatar)}">${escapeHtml(post.initials)}</div>
        <div class="card-meta">
          <div class="card-name">${escapeHtml(post.authorName)}</div>
          <div class="mini-item-meta">${escapeHtml(formatRelativeTime(post.publishedAt || post.createdAt))}</div>
        </div>
      </div>
      <div class="card-body">
        <div class="community-card-tags">
          <span class="mini-chip">${escapeHtml(post.clubLabel)}</span>
          <span class="mini-chip">${escapeHtml(`${post.primaryLabel}: ${post.primaryValue}`)}</span>
        </div>
        <div class="card-title">${escapeHtml(post.title)}</div>
        ${post.body.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("")}
        <div class="community-detail-row">
          <span class="community-detail-label">${escapeHtml(post.extraLabel)}</span>
          <strong>${escapeHtml(formatCommunityPostExtraValue(post))}</strong>
        </div>
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
        ${renderDeleteLivePostButton(post, FEED_MODULE_COMMUNITY)}
      </div>
    </article>
  `;
}

function formatCommunityPostExtraValue(post) {
  const value = String(post.extraValue || "").trim();
  if (!value) {
    return "";
  }
  if (post.extraType === "datetime") {
    const parsed = new Date(value);
    if (!Number.isNaN(parsed.getTime())) {
      return parsed.toLocaleString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
      });
    }
  }
  return value;
}

async function submitCommunityPost(form) {
  const clubKey = String(form?.dataset?.clubKey || state.communityClubKey || "").trim();
  const club = appData.communityClubs.find((item) => item.key === clubKey);
  if (!club || !club.joined) {
    showToast("Join the club before posting there.");
    return;
  }

  const formData = new FormData(form);
  const primaryValue = String(formData.get("primary_value") || "").trim();
  const headline = String(formData.get("headline") || "").trim();
  const body = String(formData.get("body") || "").trim();
  const extraValue = String(formData.get("extra_value") || "").trim();
  if (!primaryValue || !headline || !body || !extraValue) {
    showToast("Please complete all club post fields.");
    return;
  }

  communityPostsSubmittingKey = clubKey;
  renderCommunityPanel();
  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
      method: "POST",
      body: {
        title: headline,
        body,
        module: FEED_MODULE_COMMUNITY,
        kind: "update",
        topic: clubKey,
        metadata: {
          community_primary_value: primaryValue,
          community_extra_value: extraValue,
        },
      },
    });

    if (payload.post) {
      const nextPost = mapCommunityPost(payload.post);
      const currentPosts = Array.isArray(appData.communityPostsByClub[clubKey]) ? appData.communityPostsByClub[clubKey] : [];
      appData.communityPostsByClub[clubKey] = sortBulletinPostsNewestFirst([nextPost, ...currentPosts]);
      form.reset();
      renderCommunityPanel();
      showToast("Club post published.");
      return;
    }

    showToast("Club post published.");
  } catch (error) {
    showToast(error.message || "Could not publish the club post.");
  } finally {
    communityPostsSubmittingKey = "";
    renderCommunityPanel();
  }
}

function renderProfileCoinBank() {
  const container = document.getElementById("profile-coin-bank");
  if (!container) {
    return;
  }

  const monthlySummary = appData.storeBalance.monthly_summary && typeof appData.storeBalance.monthly_summary === "object"
    ? appData.storeBalance.monthly_summary
    : {};
  const openingBalance = Number(monthlySummary.opening_balance || 0);
  const earnedThisMonth = Number(monthlySummary.earned_this_month || 0);
  const spentThisMonth = Number(monthlySummary.spent_this_month || 0);
  const expiredThisMonth = Number(monthlySummary.expired_this_month || 0);
  const closingBalance = Number(monthlySummary.closing_balance || 0);

  container.innerHTML = `
    <p class="widget-kicker">Acuite Coin Bank</p>
    <div class="coin-bank-balance-line">
      <span><strong>Opening Balance</strong>: ${escapeHtml(String(openingBalance))}</span>
      <span class="coin-bank-separator">|</span>
      <span><strong>Earned this month</strong>: ${escapeHtml(String(earnedThisMonth))}</span>
      <span class="coin-bank-separator">|</span>
      <span><strong>Spent this month</strong>: ${escapeHtml(String(spentThisMonth))}</span>
      <span class="coin-bank-separator">|</span>
      <span><strong>Expired this month</strong>: ${escapeHtml(String(expiredThisMonth))}</span>
      <span class="coin-bank-separator">|</span>
      <span><strong>Closing Balance</strong>: ${escapeHtml(String(closingBalance))}</span>
    </div>
    <div class="mini-item-meta">Unused balance expires on 31 March or on the employee’s day of exit.</div>
  `;
}

function renderCeoDeskLikeButton() {
  const button = document.getElementById("ceo-desk-like-btn");
  if (!button) {
    return;
  }
  const currentMessage = getPrimaryCeoDeskMessage();
  const viewingArchive = Boolean(selectedCeoDeskArchiveKey);
  const liked = Boolean(currentMessage.currentUserHasReacted);
  const totalLikes = Number(currentMessage.reactionCount || 0);
  button.textContent = viewingArchive
    ? `Current message likes (${totalLikes})`
    : `${liked ? "Liked" : "Like"} (${totalLikes})`;
  button.classList.toggle("liked", liked);
  button.disabled = viewingArchive;
  if (viewingArchive) {
    button.removeAttribute("data-action");
    button.removeAttribute("data-id");
    return;
  }
  button.dataset.action = currentMessage.sourceId ? "toggle-live-reaction" : "toggle-like";
  button.dataset.id = String(currentMessage.sourceId || CEO_DESK_EDITORIAL.id);
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

function renderBirthdays() {
  const container = document.getElementById("birthdays-list");
  if (!container) {
    return;
  }
  container.innerHTML = appData.birthdays.length ? appData.birthdays.map((person) => `
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
  const container = document.getElementById("anniversaries-list");
  if (!container) {
    return;
  }
  container.innerHTML = appData.anniversaries.length ? appData.anniversaries.map((person) => `
    <div class="bday-item">
      <div class="bday-avatar" style="background:${gradientValue(person.gradient || gradientKeyFromText(person.name))}">${escapeHtml(person.initials)}</div>
      <div class="bday-info">
        <div class="name">${escapeHtml(person.name)}</div>
        <div class="date ${person.highlight ? "today" : ""}">${escapeHtml(person.date_label || person.date)}${person.years ? ` - ${escapeHtml(String(person.years))} yr${person.years === 1 ? "" : "s"}` : ""}</div>
      </div>
    </div>
  `).join("") : `<div class="empty-state">Work anniversary highlights will appear here later.</div>`;
}

function renderLearningSummary() {
  const container = document.getElementById("learning-summary-grid");
  if (!container) {
    return;
  }

  const filteredBooks = getFilteredLearningBooks();
  const availableTitles = appData.learningBooks.filter((book) => Number(book.available_copies || 0) > 0).length;
  const categoryCount = new Set(appData.learningBooks.map((book) => book.category).filter(Boolean)).size;

  container.innerHTML = [
    {
      kicker: "Library",
      title: `${appData.learningBooks.length} titles`,
      copy: "Internal catalog titles available for browsing.",
    },
    {
      kicker: "Shelves",
      title: `${categoryCount} categories`,
      copy: "Grouped into shelf-style rows for easier browsing.",
    },
    {
      kicker: "Available",
      title: `${availableTitles} ready now`,
      copy: filteredBooks.length
        ? `${filteredBooks.length} titles match your current search.`
        : "Search the catalog to find the right title faster.",
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
  const meta = document.getElementById("learning-results-meta");
  if (!container || !meta) {
    return;
  }

  if (elements.learningBookSearchInput) {
    elements.learningBookSearchInput.value = state.learningBookQuery;
  }

  if (learningLoadError) {
    meta.textContent = "Library load issue";
    container.innerHTML = `<div class="empty-state">${escapeHtml(learningLoadError)}</div>`;
    return;
  }

  const books = getFilteredLearningBooks();
  meta.textContent = appData.learningBooks.length
    ? `${books.length} of ${appData.learningBooks.length} titles shown${learningShowingCachedData ? ` · saved copy${learningCachedAt ? ` · updated ${formatRelativeTime(learningCachedAt)}` : ""}` : ""}`
    : "Live Acuité library catalog";

  if (!appData.learningBooks.length) {
    container.innerHTML = `
      <div class="empty-state">
        The book catalog is empty right now. Once admins upload titles in the backend, they will appear here.
      </div>
    `;
    return;
  }

  if (!books.length) {
    container.innerHTML = `
      <div class="empty-state">
        No titles match that search. Try a broader title or author search.
      </div>
    `;
    return;
  }

  const groupedBooks = groupLearningBooksByCategory(books);
  container.innerHTML = groupedBooks.map(([category, items]) => renderLearningShelf(category, items)).join("");
}

function renderLearningBookCard(book) {
  const statusText = book.available_copies > 0
    ? `${book.available_copies} of ${book.total_copies} available`
    : "Currently unavailable";
  const coverHeading = book.author || book.title;
  const likeCount = Number(book.like_count || 0);
  const likedClass = book.current_user_has_liked ? "liked" : "";
  const likeLabel = `${likeCount} like${likeCount === 1 ? "" : "s"}`;
  const likeBadgeMarkup = `
    <button
      type="button"
      class="learning-book-like ${likedClass}"
      data-action="toggle-book-like"
      data-id="${escapeHtml(String(book.id))}"
      aria-label="${escapeHtml(book.current_user_has_liked ? `Unlike ${book.title}` : `Like ${book.title}`)}"
      title="${escapeHtml(book.current_user_has_liked ? "Unlike" : "Like")}"
    >
      <span class="learning-book-like-heart" aria-hidden="true">${heartIcon()}</span>
      <span class="learning-book-like-count">${escapeHtml(String(likeCount))}</span>
      <span class="sr-only">${escapeHtml(likeLabel)}</span>
    </button>
  `;

  const coverMarkup = book.cover_url
    ? `${likeBadgeMarkup}<img src="${escapeHtml(book.cover_url)}" alt="${escapeHtml(book.title)} cover" class="learning-book-cover-image" loading="lazy">`
    : `<div class="learning-book-cover-fallback" style="background:${gradientValue(gradientKeyFromText(`${book.title}-${book.author}`))}">
        ${likeBadgeMarkup}
        <span class="learning-book-cover-category">${escapeHtml(book.category || "Library")}</span>
        <strong>${escapeHtml(coverHeading)}</strong>
      </div>`;
  const note = book.review_quote || book.summary || "Available in the internal library catalog.";
  const locationLine = [book.office_location, book.shelf_area, book.shelf_label].filter(Boolean).join(" | ");

  return `
    <article class="learning-book-card" id="book-${book.id}">
      <div class="learning-book-cover">
        ${coverMarkup}
      </div>
      <div class="learning-book-body">
        <div class="learning-book-headline">
          <span class="tool-status ${book.available_copies > 0 ? "live" : "planned"}">${escapeHtml(statusText)}</span>
          ${book.catalog_number ? `<span class="mini-item-meta">Book ${escapeHtml(book.catalog_number)}</span>` : ""}
        </div>
        <h3>${escapeHtml(book.title)}</h3>
        <p class="learning-book-note">${escapeHtml(note)}</p>
        <div class="learning-book-meta">
          <span class="mini-item-meta">${escapeHtml(locationLine || "Library catalog")}</span>
        </div>
      </div>
    </article>
  `;
}

function groupLearningBooksByCategory(books) {
  const groups = new Map();
  books.forEach((book) => {
    const category = book.category || "General Reading";
    if (!groups.has(category)) {
      groups.set(category, []);
    }
    groups.get(category).push(book);
  });
  return Array.from(groups.entries()).sort((left, right) => left[0].localeCompare(right[0]));
}

function renderLearningShelf(category, books) {
  return `
    <section class="learning-shelf">
      <div class="learning-shelf-head">
        <h3>${escapeHtml(category)}</h3>
        <span class="mini-item-meta">${escapeHtml(`${books.length} title${books.length === 1 ? "" : "s"}`)}</span>
      </div>
      <div class="learning-shelf-row">
        ${books.map(renderLearningBookCard).join("")}
      </div>
    </section>
  `;
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
        module: FEED_MODULE_BULLETIN,
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
  const livePost = findLivePostById(postId);
  const confirmed = window.confirm("Delete this post?");
  if (!confirmed) {
    return;
  }
  try {
    await window.AcuiteConnectAuth.apiRequest(`/api/feed/posts/${postId}/`, {
      method: "DELETE",
    });
    const reloadTasks = [
      loadBulletinPosts(),
      loadMyPosts(),
    ];
    if (moduleName === FEED_MODULE_COMMUNITY && livePost?.clubKey) {
      reloadTasks.push(loadCommunityPosts(livePost.clubKey, { force: true }));
    }
    await Promise.all(reloadTasks);
    renderAll();
    showToast(
      moduleName === FEED_MODULE_BULLETIN
        ? "Bulletin post deleted."
        : moduleName === FEED_MODULE_COMMUNITY
          ? "Club post deleted."
          : "Post deleted.",
    );
  } catch (error) {
    showToast(error.message || "Could not delete the post.");
  }
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
  if (elements.searchResults) {
    elements.searchResults.hidden = true;
  }
}

function useSearchResult(result) {
  if (elements.searchInput) {
    elements.searchInput.value = result.title;
  }
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
  const bulletin = getVisibleBulletinBoardPosts().map((post) => ({
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

  const books = appData.learningBooks.map((book) => ({
    title: book.title,
    subtitle: `${book.author} - Library`,
    type: "book",
    tab: "library",
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
  const myPosts = appData.myPosts.map((post) => ({
    title: post.title,
    subtitle: `${post.moderationLabel} - My Posts`,
    type: "submission",
    tab: "my-posts",
    targetId: post.id,
    searchText: [post.title, post.submissionLabel, post.metaLine, post.moderationLabel].filter(Boolean).join(" ").toLowerCase(),
  }));

  return [...bulletin, ...directory, ...books, ...store, ...myPosts];
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

function mapBulletinPost(post) {
  const metadata = post.metadata || {};
  const author = post.author || {};
  const category = (metadata.bulletin_category || post.topic || "announcements").toLowerCase();
  const authorName = author.name || "Acuité Ratings & Research";

  return {
    id: `bulletin-post-${post.id}`,
    sourceId: post.id,
    module: String(post.module || FEED_MODULE_BULLETIN),
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
    homeAnnouncementTag: String(metadata.home_announcement_tag || "").trim(),
    homeAnnouncementType: String(metadata.home_announcement_type || "").trim(),
    townHallDetails: metadata.home_announcement_town_hall && typeof metadata.home_announcement_town_hall === "object"
      ? metadata.home_announcement_town_hall
      : null,
    bulletinChannel: String(metadata.bulletin_channel || "").trim(),
    ceoDeskSubjectLine: String(metadata.ceo_desk_subject_line || "").trim(),
    userSubmission: Boolean(metadata.user_submission),
    bulletinCard: metadata.bulletin_card && typeof metadata.bulletin_card === "object" ? metadata.bulletin_card : null,
    authorName,
    authorMeta: [author.title, author.location].filter(Boolean).join(" | ") || "Company bulletin",
    initials: author.initials || initialsFromName(authorName),
    avatar: gradientKeyFromText(`${authorName}-${category}`),
    postedAtLabel: formatRelativeTime(post.published_at || post.created_at),
    publishedAt: post.published_at || "",
    createdAt: post.created_at || "",
    allowComments: Boolean(post.allow_comments),
    commentCount: post.comment_count || 0,
    reactionCount: post.reaction_count || 0,
    currentUserHasReacted: Boolean(post.current_user_has_reacted),
    canDelete: Boolean(post.viewer_can_delete),
    isAuthor: Boolean(post.viewer_is_author),
  };
}

function bulletinPostTimestamp(post) {
  const value = post?.publishedAt || post?.createdAt || "";
  const parsed = new Date(value).getTime();
  return Number.isFinite(parsed) ? parsed : 0;
}

function isBulletinPostWithinRetention(post, days = BULLETIN_BOARD_RETENTION_DAYS) {
  const timestamp = bulletinPostTimestamp(post);
  if (!timestamp) {
    return true;
  }
  const cutoff = Date.now() - (days * 24 * 60 * 60 * 1000);
  return timestamp >= cutoff;
}

function sortBulletinPostsNewestFirst(items) {
  return items.slice().sort((left, right) => bulletinPostTimestamp(right) - bulletinPostTimestamp(left));
}

function getVisibleBulletinBoardPosts() {
  return sortBulletinPostsNewestFirst(
    appData.bulletinPosts.filter((post) => isBulletinPostWithinRetention(post)),
  );
}

function getSelectedHomeAnnouncementFilterLabel() {
  return HOME_ANNOUNCEMENT_FILTERS.find(([value]) => value === state.homeAnnouncementFilter)?.[1] || "Leadership";
}

function getHomeAnnouncementPostForTag(tag) {
  return appData.homeAnnouncementPosts
    .filter((post) => post.homeAnnouncementTag === tag)
    .sort((left, right) => new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime())[0] || null;
}

function getCurrentHomeAnnouncement() {
  return getHomeAnnouncementPostForTag(state.homeAnnouncementFilter)
    || HOME_ANNOUNCEMENTS.find((item) => item.tag === state.homeAnnouncementFilter)
    || null;
}

function syncHomeAnnouncementAdminForm(form = document.getElementById("home-announcement-admin-form")) {
  if (!form) {
    return;
  }
  const typeSelect = form.querySelector("[name='announcement_type']");
  const otherFields = document.getElementById("home-announcement-other-fields");
  const townHallFields = document.getElementById("home-announcement-townhall-fields");
  const isTownHall = (typeSelect?.value || "other") === "town_hall";

  if (otherFields) {
    otherFields.hidden = isTownHall;
    toggleFormGroupControls(otherFields, !isTownHall);
  }
  if (townHallFields) {
    townHallFields.hidden = !isTownHall;
    toggleFormGroupControls(townHallFields, isTownHall);
  }

  const titleInput = form.querySelector("[name='title']");
  const bodyInput = form.querySelector("[name='body']");
  const dateInput = form.querySelector("[name='town_hall_date']");
  const timeInput = form.querySelector("[name='town_hall_time']");
  const modeInput = form.querySelector("[name='town_hall_mode']");
  const venueInput = form.querySelector("[name='town_hall_venue']");

  if (titleInput) {
    titleInput.required = !isTownHall;
  }
  if (bodyInput) {
    bodyInput.required = !isTownHall;
  }
  if (dateInput) {
    dateInput.required = isTownHall;
  }
  if (timeInput) {
    timeInput.required = isTownHall;
  }
  if (modeInput) {
    modeInput.required = isTownHall;
  }
  if (venueInput) {
    venueInput.required = isTownHall;
  }
}

function toggleFormGroupControls(group, enabled) {
  group.querySelectorAll("input, textarea, select").forEach((control) => {
    control.disabled = !enabled;
  });
}

function mapHomeAnnouncementPost(post) {
  if (post.homeAnnouncementType === "town_hall" && post.townHallDetails) {
    return buildTownHallAnnouncementFromPost(post);
  }

  return {
    id: post.id,
    sourceId: post.sourceId,
    eyebrow: getSelectedHomeAnnouncementFilterLabel(),
    type: getSelectedHomeAnnouncementFilterLabel(),
    format: "Connect",
    title: post.title,
    summary: post.body[0] || "",
    dateLabel: post.metaLines[0] || "Published on Connect",
    timeLabel: post.postedAtLabel || "Now live",
    venueLabel: "Connect announcement",
    hostLabel: post.authorName || "Acuité Ratings & Research",
    audienceLabel: "Visible to all employees",
    countdownLabel: post.postedAtLabel || "",
    baseMetrics: {
      likes: Number(post.reactionCount || 0),
    },
    currentUserHasReacted: Boolean(post.currentUserHasReacted),
    isLive: true,
  };
}

function buildTownHallAnnouncementFromPost(post) {
  const details = post.townHallDetails || {};
  return {
    id: post.id,
    sourceId: post.sourceId,
    eyebrow: getSelectedHomeAnnouncementFilterLabel(),
    type: "Town Hall",
    format: formatTownHallModeLabel(details.mode) || "Town Hall",
    title: TOWN_HALL_GENERIC_CONTENT.title,
    summary: TOWN_HALL_GENERIC_CONTENT.summary,
    dateLabel: formatAnnouncementLongDate(details.date) || post.metaLines[0] || "Date to be announced",
    timeLabel: String(details.time || "").trim() || "Time to be announced",
    venueLabel: normalizeTownHallVenueLabel(details.venue),
    hostLabel: TOWN_HALL_GENERIC_CONTENT.hostLabel,
    audienceLabel: TOWN_HALL_GENERIC_CONTENT.audienceLabel,
    countdownLabel: getTownHallCountdownLabel(details.date),
    baseMetrics: {
      likes: Number(post.reactionCount || 0),
    },
    currentUserHasReacted: Boolean(post.currentUserHasReacted),
    isLive: true,
  };
}

function getCeoDeskPosts() {
  return appData.ceoDeskPosts
    .filter((post) => post.bulletinChannel === "ceo_desk")
    .sort((left, right) => new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime());
}

function getCurrentCeoDeskMessage() {
  const archivedMessage = getSelectedCeoDeskArchiveMessage();
  if (archivedMessage) {
    return archivedMessage;
  }

  return getPrimaryCeoDeskMessage();
}

function getPrimaryCeoDeskMessage() {
  const livePost = getCeoDeskPosts()[0];
  if (!livePost) {
    const liked = state.likedPostIds.includes(CEO_DESK_EDITORIAL.id);
    return {
      ...DEFAULT_CEO_DESK_MESSAGE,
      body: DEFAULT_CEO_DESK_MESSAGE.body.slice(),
      sourceId: "",
      reactionCount: CEO_DESK_EDITORIAL.baseLikes + (liked ? 1 : 0),
      currentUserHasReacted: liked,
    };
  }
  return {
    date: livePost.metaLines[0] || formatDisplayDate(livePost.createdAt) || DEFAULT_CEO_DESK_MESSAGE.date,
    title: livePost.title || DEFAULT_CEO_DESK_MESSAGE.title,
    meta: "",
    body: Array.isArray(livePost.body) && livePost.body.length ? livePost.body : DEFAULT_CEO_DESK_MESSAGE.body,
    sourceId: livePost.sourceId,
    reactionCount: Number(livePost.reactionCount || 0),
    currentUserHasReacted: Boolean(livePost.currentUserHasReacted),
  };
}

function getCeoDeskArchiveItems() {
  const livePosts = getCeoDeskPosts();
  const fallbackItems = DEFAULT_CEO_DESK_ARCHIVE.map((item) => ({
    ...item,
    archiveKey: buildCeoDeskArchiveKey(item),
  }));

  if (!livePosts.length) {
    return fallbackItems.slice(0, CEO_DESK_ARCHIVE_LIMIT);
  }
  const liveArchiveItems = livePosts.slice(1, CEO_DESK_ARCHIVE_LIMIT + 1).map((post) => ({
    datePosted: post.metaLines[0] || formatCeoDeskPostedDate(post.createdAt),
    headline: post.title || "MD & CEO message",
    subjectLine: post.ceoDeskSubjectLine || "",
    body: Array.isArray(post.body) && post.body.length ? post.body : ["Archived message details are not available in this build."],
    sourceId: post.sourceId,
    reactionCount: Number(post.reactionCount || 0),
    currentUserHasReacted: Boolean(post.currentUserHasReacted),
    archiveKey: buildCeoDeskArchiveKey(post),
  }));

  const liveArchiveKeys = new Set(liveArchiveItems.map((item) => item.archiveKey));
  return [
    ...liveArchiveItems,
    ...fallbackItems.filter((item) => !liveArchiveKeys.has(item.archiveKey)),
  ].slice(0, CEO_DESK_ARCHIVE_LIMIT);
}

function buildCeoDeskArchiveKey(item) {
  const sourceId = String(item?.sourceId || "").trim();
  if (sourceId) {
    return `source:${sourceId}`;
  }
  return [
    String(item?.datePosted || item?.date || "").trim(),
    String(item?.headline || item?.title || "").trim(),
    String(item?.subjectLine || item?.subject_line || "").trim(),
  ].join("|");
}

function getSelectedCeoDeskArchiveMessage() {
  if (!selectedCeoDeskArchiveKey) {
    return null;
  }
  const archiveItem = getCeoDeskArchiveItems().find((item) => item.archiveKey === selectedCeoDeskArchiveKey);
  if (!archiveItem) {
    selectedCeoDeskArchiveKey = "";
    return null;
  }
  return {
    date: archiveItem.datePosted || "",
    title: archiveItem.headline || "MD & CEO message",
    meta: "",
    body: Array.isArray(archiveItem.body) && archiveItem.body.length ? archiveItem.body : DEFAULT_CEO_DESK_MESSAGE.body,
    sourceId: archiveItem.sourceId || "",
    reactionCount: Number(archiveItem.reactionCount || 0),
    currentUserHasReacted: Boolean(archiveItem.currentUserHasReacted),
  };
}

function mapMyPostSubmission(post) {
  const metadata = post.metadata || {};
  const moderationStatus = String(post.moderation_status || "pending_review");
  return {
    id: `my-post-${post.id}`,
    sourceId: post.id,
    title: post.title || "Untitled post",
    submissionLabel: String(metadata.submission_label || "Employee post"),
    metaLine: Array.isArray(metadata.bulletin_meta_lines) ? String(metadata.bulletin_meta_lines[0] || "").trim() : "",
    moderationStatus,
    moderationLabel:
      moderationStatus === "published"
        ? "Approved and live"
        : moderationStatus === "rejected"
          ? "Not approved"
          : "Waiting for admin review",
    commentCount: Number(post.comment_count || 0),
    reactionCount: Number(post.reaction_count || 0),
    createdAt: post.created_at || "",
    publishedAt: post.published_at || "",
  };
}

function mapCommunityPost(post) {
  const metadata = post.metadata || {};
  const author = post.author || {};
  const authorName = author.name || author.email || "Employee";
  const bodyParagraphs = String(post.body || "")
    .split(/\n{2,}/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);

  return {
    id: `community-post-${post.id}`,
    sourceId: post.id,
    module: post.module || FEED_MODULE_COMMUNITY,
    title: post.title || "Club update",
    body: bodyParagraphs.length ? bodyParagraphs : [String(post.body || "").trim()].filter(Boolean),
    authorName,
    initials: author.initials || initialsFromName(authorName),
    avatar: gradientKeyFromText(`${metadata.community_club_key || post.topic}-${authorName}`),
    commentCount: Number(post.comment_count || 0),
    reactionCount: Number(post.reaction_count || 0),
    currentUserHasReacted: Boolean(post.current_user_has_reacted),
    createdAt: post.created_at || "",
    publishedAt: post.published_at || "",
    allowComments: post.allow_comments !== false,
    canDelete: Boolean(post.viewer_can_delete),
    clubKey: String(metadata.community_club_key || post.topic || "").trim(),
    clubLabel: String(metadata.community_club_label || "Community").trim(),
    primaryLabel: String(metadata.community_primary_label || "Title").trim(),
    primaryValue: String(metadata.community_primary_value || "").trim(),
    extraLabel: String(metadata.community_extra_label || "Additional detail").trim(),
    extraValue: String(metadata.community_extra_value || "").trim(),
    extraType: String(metadata.community_extra_type || "text").trim(),
  };
}

function getSelectedMyPostType() {
  if (!elements.myPostsTypeSelect) {
    return null;
  }
  return MY_POST_TYPES.find((item) => item.key === String(elements.myPostsTypeSelect.value || "").trim()) || null;
}

function isPraiseSomeoneMyPostType(selectedType = getSelectedMyPostType()) {
  return Boolean(selectedType && selectedType.key === "praise_someone");
}

function getPraiseSomeoneLocation(person) {
  return person?.branchLocation || person?.office || person?.city || "";
}

function buildPraiseSomeoneHeadline(person) {
  return [person?.name || "", person?.role || "", getPraiseSomeoneLocation(person)].filter(Boolean).join(" | ");
}

function hideMyPostsPersonSuggestions() {
  if (!elements.myPostsPersonSuggestions) {
    return;
  }
  elements.myPostsPersonSuggestions.hidden = true;
  elements.myPostsPersonSuggestions.innerHTML = "";
}

function getMyPostsPersonSuggestions(query) {
  const trimmedQuery = String(query || "").trim().toLowerCase();
  const normalizedQuery = trimmedQuery.replace(/[^a-z0-9]+/g, " ");
  if (!trimmedQuery) {
    return [];
  }

  return appData.directory
    .filter((person) => person.name && person.role)
    .filter((person) => {
      const searchText = [
        person.name,
        person.role,
        getPraiseSomeoneLocation(person),
        buildPraiseSomeoneHeadline(person),
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      const normalizedSearchText = searchText.replace(/[^a-z0-9]+/g, " ");
      return searchText.includes(trimmedQuery) || normalizedSearchText.includes(normalizedQuery);
    })
    .sort((left, right) => {
      const leftName = String(left.name || "").toLowerCase();
      const rightName = String(right.name || "").toLowerCase();
      const leftStarts = leftName.startsWith(trimmedQuery) ? 0 : 1;
      const rightStarts = rightName.startsWith(trimmedQuery) ? 0 : 1;
      if (leftStarts !== rightStarts) {
        return leftStarts - rightStarts;
      }
      return leftName.localeCompare(rightName);
    })
    .slice(0, 8);
}

function renderMyPostsPersonSuggestions() {
  if (!elements.myPostsPersonSuggestions || !elements.myPostsTitleInput || !elements.myPostsSelectedPersonId) {
    return;
  }
  if (!isPraiseSomeoneMyPostType()) {
    hideMyPostsPersonSuggestions();
    return;
  }

  const query = String(elements.myPostsTitleInput.value || "").trim();
  const selectedHeadline = String(elements.myPostsTitleInput.dataset.selectedHeadline || "").trim();
  const selectedPersonId = String(elements.myPostsSelectedPersonId.value || "").trim();
  if (!query) {
    hideMyPostsPersonSuggestions();
    return;
  }
  if (selectedPersonId && selectedHeadline && query === selectedHeadline) {
    hideMyPostsPersonSuggestions();
    return;
  }

  const suggestions = getMyPostsPersonSuggestions(query);
  if (!suggestions.length) {
    elements.myPostsPersonSuggestions.hidden = false;
    elements.myPostsPersonSuggestions.innerHTML = appData.directory.length
      ? `<div class="typeahead-empty">No matching employee found.</div>`
      : `<div class="typeahead-empty">${escapeHtml(directoryLoadError || "Directory is still loading. Please try again in a moment.")}</div>`;
    return;
  }

  elements.myPostsPersonSuggestions.hidden = false;
  elements.myPostsPersonSuggestions.innerHTML = suggestions.map((person) => `
    <button
      type="button"
      class="typeahead-option"
      data-action="select-my-posts-person"
      data-id="${escapeHtml(String(person.sourceUserId))}"
    >
      <strong>${escapeHtml(person.name)}</strong>
      <span>${escapeHtml([person.role, getPraiseSomeoneLocation(person)].filter(Boolean).join(" | "))}</span>
    </button>
  `).join("");
}

function handleMyPostsTitleInput() {
  if (!elements.myPostsTitleInput || !elements.myPostsSelectedPersonId) {
    return;
  }
  if (!isPraiseSomeoneMyPostType()) {
    hideMyPostsPersonSuggestions();
    return;
  }

  const currentValue = String(elements.myPostsTitleInput.value || "").trim();
  const selectedHeadline = String(elements.myPostsTitleInput.dataset.selectedHeadline || "").trim();
  if (!currentValue || currentValue !== selectedHeadline) {
    elements.myPostsSelectedPersonId.value = "";
    elements.myPostsTitleInput.dataset.selectedHeadline = "";
  }
  renderMyPostsPersonSuggestions();
}

function selectMyPostsPerson(personId) {
  if (!elements.myPostsTitleInput || !elements.myPostsSelectedPersonId) {
    return;
  }
  const person = appData.directory.find((item) => String(item.sourceUserId) === String(personId));
  if (!person) {
    showToast("Could not find that employee in the directory.");
    return;
  }
  const headline = buildPraiseSomeoneHeadline(person);
  elements.myPostsTitleInput.value = headline;
  elements.myPostsTitleInput.dataset.selectedHeadline = headline;
  elements.myPostsSelectedPersonId.value = String(person.sourceUserId);
  hideMyPostsPersonSuggestions();
}

function getFilteredLearningBooks() {
  const query = state.learningBookQuery.trim().toLowerCase();
  let books = appData.learningBooks.slice();

  if (state.learningBookFilter === "available") {
    books = books.filter((book) => book.available_copies > 0);
  }

  if (!query) {
    return books;
  }

  return books.filter((book) => {
    return [book.title, book.author, book.summary, book.category, book.office_location, book.shelf_area, book.shelf_label]
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

function switchTab(tabId) {
  state.activeTab = ENABLED_TABS.has(tabId) ? tabId : "home";
  saveState();
  if (state.activeTab === "community" && !communityLoading && !appData.communityClubs.length) {
    void loadCommunityData();
  }
  hideSearchResults();
  renderPanels();
  window.requestAnimationFrame(() => {
    try {
      renderAll();
    } catch (error) {
      console.error("Could not fully render the selected tab.", error);
      renderPanels();
    }
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
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

function syncMyPostsComposer() {
  if (!elements.myPostsTypeSelect || !elements.myPostsFields) {
    return;
  }

  const selectedType = getSelectedMyPostType();
  elements.myPostsFields.hidden = !selectedType;
  if (!selectedType) {
    hideMyPostsPersonSuggestions();
    return;
  }

  if (elements.myPostsTitleLabel) {
    elements.myPostsTitleLabel.textContent = selectedType.titleLabel;
  }
  if (elements.myPostsTitleInput) {
    elements.myPostsTitleInput.placeholder = selectedType.titlePlaceholder;
    elements.myPostsTitleInput.value = "";
    elements.myPostsTitleInput.dataset.selectedHeadline = "";
  }
  if (elements.myPostsMetaLabel) {
    elements.myPostsMetaLabel.textContent = selectedType.metaLabel;
  }
  if (elements.myPostsMetaInput) {
    elements.myPostsMetaInput.placeholder = selectedType.metaPlaceholder;
  }
  if (elements.myPostsBodyLabel) {
    elements.myPostsBodyLabel.textContent = selectedType.bodyLabel;
  }
  if (elements.myPostsBodyInput) {
    elements.myPostsBodyInput.placeholder = selectedType.bodyPlaceholder;
  }
  if (elements.myPostsSelectedPersonId) {
    elements.myPostsSelectedPersonId.value = "";
  }
  if (elements.myPostsHelpCopy) {
    elements.myPostsHelpCopy.textContent = `${selectedType.label}. Your post will go to the admin dashboard first for approval.`;
    elements.myPostsHelpCopy.hidden = Boolean(selectedType.hideHelpCopy);
  }
  hideMyPostsPersonSuggestions();
}

async function submitMyPost() {
  if (!currentUserCanCreatePosts()) {
    showToast("Your posting access is currently disabled.");
    return;
  }

  const formData = new FormData(elements.myPostsForm);
  const submissionKey = String(formData.get("submission_key") || "").trim();
  const selectedType = MY_POST_TYPES.find((item) => item.key === submissionKey);
  let title = String(formData.get("title") || "").trim();
  const metaLine = String(formData.get("meta_line") || "").trim();
  const body = String(formData.get("body") || "").trim();
  const selectedPersonId = String(formData.get("selected_person_id") || "").trim();

  if (!selectedType || !title || !body) {
    showToast("Choose the post type, add a headline, and write the details.");
    return;
  }

  const metadata = {
    bulletin_category: "employee_posts",
    submission_key: selectedType.key,
    submission_label: selectedType.label,
    bulletin_meta_lines: metaLine ? [metaLine] : [],
    user_submission: true,
  };

  if (selectedType.key === "praise_someone") {
    const selectedPerson = appData.directory.find((person) => String(person.sourceUserId) === selectedPersonId);
    if (!selectedPerson) {
      showToast("Select a person from the list before submitting.");
      return;
    }
    title = buildPraiseSomeoneHeadline(selectedPerson);
    metadata.praised_person = {
      user_id: selectedPerson.sourceUserId,
      name: selectedPerson.name,
      designation: selectedPerson.role,
      location: getPraiseSomeoneLocation(selectedPerson),
    };
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest("/api/feed/posts/", {
      method: "POST",
      body: {
        title,
        body,
        module: FEED_MODULE_EMPLOYEE_POSTS,
        kind: "update",
        topic: "employee_submission",
        metadata,
      },
    });

    if (payload.post) {
      appData.myPosts.unshift(mapMyPostSubmission(payload.post));
      elements.myPostsForm.reset();
      syncMyPostsComposer();
      renderMyPostsPanel();
      showToast("Your post is now waiting for admin approval.");
      return;
    }

    showToast("Your post was submitted.");
  } catch (error) {
    showToast(error.message || "Could not submit your post.");
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
      await loadStoreData();
      renderHomeAnnouncement();
      renderBulletinPanel();
      renderCommunityPanel();
      renderCeoDeskLikeButton();
      renderProfileCoinBank();
      renderProfile();
      showToast(payload.reacted ? "Appreciation recorded." : "Appreciation removed.");
      return;
    }

    showToast("Reaction updated.");
  } catch (error) {
    showToast(error.message || "Could not update appreciation.");
  }
}

async function toggleBookLike(bookId) {
  if (!window.AcuiteConnectAuth?.apiRequest) {
    showToast("Sign in again to like this book.");
    return;
  }

  const targetId = Number(bookId);
  if (!targetId) {
    return;
  }

  try {
    const payload = await window.AcuiteConnectAuth.apiRequest(`/api/learning/books/${targetId}/likes/toggle/`, {
      method: "POST",
    });
    if (!payload?.book) {
      throw new Error("Missing updated book payload.");
    }
    appData.learningBooks = appData.learningBooks.map((book) => (
      Number(book.id) === targetId ? { ...book, ...payload.book } : book
    ));
    saveLearningCache();
    renderAll();
  } catch (error) {
    showToast(error.message || "Could not update the book like right now.");
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
    activeTab: saved.activeTab === "clubs-learning"
      ? "library"
      : (typeof saved.activeTab === "string" ? saved.activeTab : defaultState.activeTab),
    homeAnnouncementFilter: (
      typeof saved.homeAnnouncementFilter === "string"
      && HOME_ANNOUNCEMENT_FILTERS.some(([value]) => value === saved.homeAnnouncementFilter)
    )
      ? saved.homeAnnouncementFilter
      : defaultState.homeAnnouncementFilter,
    brochureBuilderSelectedIds: Array.isArray(saved.brochureBuilderSelectedIds)
      ? saved.brochureBuilderSelectedIds.filter((value) => typeof value === "string")
      : defaultState.brochureBuilderSelectedIds.slice(),
    storeFilter: (
      typeof saved.storeFilter === "string"
      && ["all", ...Object.keys(STORE_CATEGORY_LABELS)].includes(saved.storeFilter)
    )
      ? saved.storeFilter
      : defaultState.storeFilter,
    learningBookFilter: (
      typeof saved.learningBookFilter === "string"
      && ["all", "available"].includes(saved.learningBookFilter)
    )
      ? saved.learningBookFilter
      : defaultState.learningBookFilter,
    learningBookQuery: typeof saved.learningBookQuery === "string"
      ? saved.learningBookQuery
      : defaultState.learningBookQuery,
    communityClubKey: typeof saved.communityClubKey === "string"
      ? saved.communityClubKey
      : defaultState.communityClubKey,
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
    customBulletins: Array.isArray(saved.customBulletins) ? saved.customBulletins : [],
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

function readDirectoryCache() {
  try {
    const raw = window.localStorage.getItem(DIRECTORY_CACHE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (error) {
    return null;
  }
}

function readCeoDeskCache() {
  try {
    const raw = window.localStorage.getItem(CEO_DESK_CACHE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (error) {
    return null;
  }
}

function hydrateDirectoryCache() {
  const saved = readDirectoryCache();
  if (!saved || !Array.isArray(saved.results)) {
    return false;
  }

  appData.directory = saved.results;
  directoryFilterOptions = {
    company: Array.isArray(saved.filters?.company) ? saved.filters.company : [],
    location: Array.isArray(saved.filters?.location) ? saved.filters.location : [],
    department: Array.isArray(saved.filters?.department) ? saved.filters.department : [],
  };
  directoryCachedAt = typeof saved.cachedAt === "string" ? saved.cachedAt : "";
  directoryShowingCachedData = true;
  return true;
}

function hydrateCeoDeskCache() {
  const saved = readCeoDeskCache();
  if (!saved || !Array.isArray(saved.results)) {
    return false;
  }

  appData.ceoDeskPosts = saved.results;
  ceoDeskCachedAt = typeof saved.cachedAt === "string" ? saved.cachedAt : "";
  ceoDeskShowingCachedData = true;
  return true;
}

function readLearningCache() {
  try {
    const raw = window.localStorage.getItem(LEARNING_CACHE_KEY);
    if (!raw) {
      return null;
    }
    const parsed = JSON.parse(raw);
    const currentBuildNumber = getCurrentBuildNumber();
    if (parsed && currentBuildNumber && parsed.buildNumber !== currentBuildNumber) {
      window.localStorage.removeItem(LEARNING_CACHE_KEY);
      return null;
    }
    return parsed;
  } catch (error) {
    return null;
  }
}

function hydrateLearningCache() {
  const saved = readLearningCache();
  if (!saved || !Array.isArray(saved.results)) {
    return false;
  }

  appData.learningBooks = saved.results;
  learningCachedAt = typeof saved.cachedAt === "string" ? saved.cachedAt : "";
  learningShowingCachedData = true;
  return true;
}

function saveState() {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    return;
  }
}

function saveCeoDeskCache() {
  try {
    window.localStorage.setItem(
      CEO_DESK_CACHE_KEY,
      JSON.stringify({
        cachedAt: ceoDeskCachedAt || new Date().toISOString(),
        results: appData.ceoDeskPosts,
      }),
    );
  } catch (error) {
    return;
  }
}

function saveLearningCache() {
  try {
    window.localStorage.setItem(
      LEARNING_CACHE_KEY,
      JSON.stringify({
        buildNumber: getCurrentBuildNumber(),
        cachedAt: learningCachedAt || new Date().toISOString(),
        results: appData.learningBooks,
      }),
    );
  } catch (error) {
    return;
  }
}

function saveDirectoryCache() {
  try {
    window.localStorage.setItem(
      DIRECTORY_CACHE_KEY,
      JSON.stringify({
        cachedAt: directoryCachedAt || new Date().toISOString(),
        results: appData.directory,
        filters: directoryFilterOptions,
      }),
    );
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

function createProfileBuilderDraft() {
  return {
    skills: [],
    hobbies: [],
    interestsText: "",
    photos: [],
  };
}

function createProfileDraftFromProfile(profile) {
  if (!profile) {
    return createProfileBuilderDraft();
  }
  return {
    skills: Array.isArray(profile.skills) ? profile.skills.slice(0, 3) : [],
    hobbies: Array.isArray(profile.hobbies) ? profile.hobbies.slice(0, 3) : [],
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

function renderDirectoryChips() {
  const container = document.getElementById("directory-filter-groups");
  if (!container) {
    return;
  }

  container.innerHTML = DIRECTORY_FILTER_GROUPS.map((groupId) => {
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
  const resultsMeta = document.getElementById("directory-results-meta");
  const grid = document.getElementById("directory-grid");
  if (!resultsMeta || !grid) {
    return;
  }

  if (elements.directorySearchInput) {
    elements.directorySearchInput.value = state.directoryQuery;
  }

  const query = state.directoryQuery.trim().toLowerCase();
  const selectedCompanies = state.directoryFilters.company || [];
  const selectedLocations = state.directoryFilters.location || [];
  const selectedDepartments = state.directoryFilters.department || [];
  const filtered = appData.directory.filter((person) => {
    if (selectedCompanies.length && !selectedCompanies.includes(person.company)) {
      return false;
    }
    if (selectedLocations.length && !selectedLocations.includes(person.branchLocation)) {
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
    resultsMeta.textContent = "Directory load issue";
    grid.innerHTML = `<div class="empty-state">${escapeHtml(directoryLoadError)}</div>`;
    return;
  }

  resultsMeta.textContent = appData.directory.length
    ? `${filtered.length} of ${appData.directory.length} employees shown${directoryShowingCachedData ? ` · saved copy${directoryCachedAt ? ` · updated ${formatRelativeTime(directoryCachedAt)}` : ""}` : ""}`
    : "Live employee directory";

  if (!appData.directory.length) {
    grid.innerHTML = `<div class="empty-state">The people directory will appear here once the live employee import completes.</div>`;
    return;
  }

  grid.innerHTML = filtered.length
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
        <div class="person-attributes">
          ${renderDirectoryAttributeBlock("Skills", person.skills)}
          ${renderDirectoryAttributeBlock("Hobbies", person.hobbies)}
        </div>
        <div class="person-footer">
          <span class="availability">${escapeHtml(person.contactLine)}</span>
        </div>
      </article>
    `).join("")
    : `<div class="empty-state">No people matched that filter. Try a broader company, location, or department selection.</div>`;
}

function renderDirectoryAttributeBlock(label, values) {
  const items = Array.isArray(values) ? values.filter(Boolean) : [];
  const displayValue = items.length ? items.join(" · ") : "Not added yet";
  return `
    <div class="person-attribute">
      <div class="person-attribute-label">${escapeHtml(label)}</div>
      <div class="person-attribute-value ${items.length ? "" : "empty"}">${escapeHtml(displayValue)}</div>
    </div>
  `;
}

function getIamAcuiteSourcePhotos() {
  return appData.directory
    .flatMap((person) => {
      const photos = Array.isArray(person.profilePhotos) ? person.profilePhotos.filter(Boolean).slice(0, 2) : [];
      return photos.map((photo, index) => ({
        id: `${String(person.sourceUserId || person.id || person.name)}-${index + 1}`,
        name: person.name || "Employee",
        photo,
      }));
    })
    .slice(0, IAM_ACUITE_TILE_COUNT);
}

function getIamAcuiteSignature(photos) {
  return photos.map((item) => `${item.id}:${item.photo}`).join("|");
}

function invalidateIamAcuitePoster() {
  iamAcuitePosterState = {
    signature: "",
    dataUrl: "",
    photoCount: 0,
    loading: false,
    error: "",
  };
}

function renderIamAcuitePanel() {
  const stage = document.getElementById("iam-acuite-stage");
  const meta = document.getElementById("iam-acuite-meta");
  if (!stage || !meta) {
    return;
  }

  const photos = getIamAcuiteSourcePhotos();
  const signature = getIamAcuiteSignature(photos);

  if ((iamAcuitePosterState.signature !== signature || !iamAcuitePosterState.dataUrl) && !iamAcuitePosterState.loading) {
    iamAcuitePosterState.loading = true;
    iamAcuitePosterState.error = "";
    meta.textContent = `Building a 400-tile wall from ${photos.length} real portrait${photos.length === 1 ? "" : "s"}...`;
    stage.innerHTML = `
      <div class="iam-acuite-empty">
        <strong>Building the wall</strong>
        <span>Preparing a fresh mosaic with deep-red tiles and the latest employee photos.</span>
      </div>
    `;
    void buildIamAcuitePoster(photos, signature);
    return;
  }

  if (iamAcuitePosterState.loading) {
    meta.textContent = `Building a 400-tile wall from ${photos.length} real portrait${photos.length === 1 ? "" : "s"}...`;
    if (!stage.innerHTML.trim()) {
      stage.innerHTML = `
        <div class="iam-acuite-empty">
          <strong>Building the wall</strong>
          <span>Preparing a fresh mosaic with deep-red tiles and the latest employee photos.</span>
        </div>
      `;
    }
    return;
  }

  if (iamAcuitePosterState.error) {
    meta.textContent = iamAcuitePosterState.error;
    stage.innerHTML = `
      <div class="iam-acuite-empty">
        <strong>I am Acuite</strong>
        <span>${escapeHtml(iamAcuitePosterState.error)}</span>
      </div>
    `;
    return;
  }

  meta.textContent = `${iamAcuitePosterState.photoCount} of ${IAM_ACUITE_TILE_COUNT} portrait slots are live right now.`;
  stage.innerHTML = `
    <img
      class="iam-acuite-poster"
      src="${escapeHtml(iamAcuitePosterState.dataUrl)}"
      alt="I am Acuite mosaic built from employee portraits and deep-red tiles"
    >
  `;
}

async function refreshIamAcuitePoster() {
  iamAcuitePosterState.loading = true;
  iamAcuitePosterState.error = "";
  renderAll();
  await loadDirectoryData();
  if (directoryLoadError) {
    iamAcuitePosterState.loading = false;
  }
  renderAll();
}

async function buildIamAcuitePoster(photos, signature) {
  const currentToken = ++iamAcuiteRenderToken;
  try {
    const poster = await generateIamAcuitePoster(photos);
    if (currentToken !== iamAcuiteRenderToken) {
      return;
    }
    iamAcuitePosterState = {
      signature,
      dataUrl: poster.dataUrl,
      photoCount: photos.length,
      loading: false,
      error: "",
    };
  } catch (error) {
    if (currentToken !== iamAcuiteRenderToken) {
      return;
    }
    iamAcuitePosterState = {
      signature: "",
      dataUrl: "",
      photoCount: photos.length,
      loading: false,
      error: error.message || "Could not build the portrait wall right now.",
    };
  }
  renderAll();
}

async function generateIamAcuitePoster(photos) {
  const preparedPhotos = deterministicShuffle((await Promise.all(
    photos.map((item) => prepareIamAcuiteTile(item.photo)),
  )).filter(Boolean), signatureHash(getIamAcuiteSignature(photos)) + 17);
  const width = 1500;
  const height = 960;
  const tileSize = Math.floor(width / IAM_ACUITE_COLUMNS);
  const columns = IAM_ACUITE_COLUMNS;
  const rows = IAM_ACUITE_ROWS;
  const outputCanvas = document.createElement("canvas");
  outputCanvas.width = width;
  outputCanvas.height = height;
  const outputContext = outputCanvas.getContext("2d");
  if (!outputContext) {
    throw new Error("Canvas rendering is unavailable in this browser.");
  }

  const maskCanvas = document.createElement("canvas");
  maskCanvas.width = width;
  maskCanvas.height = height;
  const maskContext = maskCanvas.getContext("2d");
  if (!maskContext) {
    throw new Error("Canvas masking is unavailable in this browser.");
  }

  drawIamAcuiteMask(maskContext, width, height, tileSize);
  const maskData = maskContext.getImageData(0, 0, width, height).data;
  const positions = [];
  for (let row = 0; row < rows; row += 1) {
    for (let column = 0; column < columns; column += 1) {
      const x = column * tileSize;
      const y = row * tileSize;
      const sampleX = Math.min(width - 1, x + Math.floor(tileSize / 2));
      const sampleY = Math.min(height - 1, y + Math.floor(tileSize / 2));
      const alphaIndex = ((sampleY * width) + sampleX) * 4 + 3;
      positions.push({
        x,
        y,
        row,
        column,
        isTextPixel: maskData[alphaIndex] > 20,
      });
    }
  }

  const hashSeed = signatureHash(getIamAcuiteSignature(photos));
  const cellProfiles = positions.map((position) => buildIamAcuiteCellProfile(position, columns, rows, hashSeed));
  const textCells = cellProfiles
    .filter((cell) => cell.isTextPixel)
    .sort((left, right) => left.scatterRank - right.scatterRank);
  const backgroundCells = cellProfiles
    .filter((cell) => !cell.isTextPixel)
    .sort((left, right) => left.scatterRank - right.scatterRank);
  const fillOrder = buildIamAcuiteFillOrder(textCells, backgroundCells);
  const selectedCells = fillOrder.slice(0, preparedPhotos.length);
  const livePlacements = assignIamAcuitePhotosToCells(selectedCells, preparedPhotos);
  const placeholderTile = createIamAcuitePlaceholderTile();

  cellProfiles.forEach((position) => {
    const placementKey = position.key;
    const liveTile = livePlacements.get(placementKey);
    const tileCanvas = liveTile
      ? renderIamAcuitePhotoTile(liveTile.photo, position)
      : placeholderTile.canvas;
    outputContext.drawImage(tileCanvas, position.x, position.y, tileSize, tileSize);
  });

  return {
    dataUrl: outputCanvas.toDataURL("image/jpeg", 0.92),
  };
}

function buildIamAcuiteCellProfile(position, columns, rows, hashSeed) {
  const columnRatio = columns > 1 ? position.column / (columns - 1) : 0.5;
  const rowRatio = rows > 1 ? position.row / (rows - 1) : 0.5;
  const centerBias = 1 - Math.min(1, Math.abs(columnRatio - 0.5) * 1.9);
  const wave = (
    Math.sin((position.column + 1) * 0.72 + hashSeed * 0.013) +
    Math.cos((position.row + 1) * 0.81 + hashSeed * 0.017)
  ) * 0.5;
  const scatterRank = hashStringToUnit(`iam-acuite:${hashSeed}:${position.row}:${position.column}`);
  const key = `${position.x}:${position.y}`;

  if (position.isTextPixel) {
    return {
      ...position,
      key,
      scatterRank,
      targetBrightness: clampNumber(170 + (centerBias * 34) + (wave * 10), 146, 228),
      targetHue: clampHue(28 + (wave * 9)),
      targetSaturation: clampNumber(58 + (centerBias * 18) + (wave * 12), 34, 90),
      brightnessRange: [132, 236],
      hueRange: [8, 56],
      saturationRange: [24, 100],
    };
  }

  return {
    ...position,
    key,
    scatterRank,
    targetBrightness: clampNumber(78 + (wave * 9), 44, 122),
    targetHue: clampHue(8 + (wave * 5)),
    targetSaturation: clampNumber(52 + (centerBias * 8) + (wave * 10), 24, 84),
    brightnessRange: [36, 132],
    hueRange: [0, 22],
    saturationRange: [18, 92],
  };
}

function buildIamAcuiteFillOrder(textCells, backgroundCells) {
  const positions = [];
  const textQueue = textCells.slice();
  const backgroundQueue = backgroundCells.slice();
  while (textQueue.length || backgroundQueue.length) {
    for (let step = 0; step < 3; step += 1) {
      if (textQueue.length) {
        positions.push(textQueue.shift());
      }
    }
    if (backgroundQueue.length) {
      positions.push(backgroundQueue.shift());
    }
  }
  return positions;
}

function assignIamAcuitePhotosToCells(cells, photos) {
  const placements = new Map();
  const remainingPhotos = photos.slice();

  cells.forEach((cell) => {
    if (!remainingPhotos.length) {
      return;
    }

    let bestIndex = 0;
    let bestScore = Number.POSITIVE_INFINITY;
    remainingPhotos.forEach((photo, index) => {
      const score = scoreIamAcuitePhotoForCell(photo, cell);
      if (score < bestScore) {
        bestScore = score;
        bestIndex = index;
      }
    });

    const [selectedPhoto] = remainingPhotos.splice(bestIndex, 1);
    if (selectedPhoto) {
      placements.set(cell.key, {
        photo: selectedPhoto,
        score: bestScore,
      });
    }
  });

  return placements;
}

function scoreIamAcuitePhotoForCell(photo, cell) {
  const brightnessPenalty = rangePenalty(photo.brightness, cell.brightnessRange[0], cell.brightnessRange[1])
    + (Math.abs(photo.brightness - cell.targetBrightness) * 0.45);
  const huePenalty = rangePenaltyHue(photo.hue, cell.hueRange[0], cell.hueRange[1])
    + (circularHueDistance(photo.hue, cell.targetHue) * 0.75);
  const saturationPenalty = rangePenalty(photo.saturation, cell.saturationRange[0], cell.saturationRange[1])
    + (Math.abs(photo.saturation - cell.targetSaturation) * 0.28);
  return brightnessPenalty + huePenalty + saturationPenalty;
}

function createIamAcuitePlaceholderTile() {
  const canvas = document.createElement("canvas");
  canvas.width = 72;
  canvas.height = 72;
  const context = canvas.getContext("2d");
  if (context) {
    context.fillStyle = IAM_ACUITE_PLACEHOLDER_COLOR;
    context.fillRect(0, 0, canvas.width, canvas.height);
  }
  return {
    id: "placeholder-deep-red",
    canvas,
    brightness: 64,
  };
}

function renderIamAcuitePhotoTile(photo, cell) {
  const sourceCanvas = photo.canvas;
  const canvas = document.createElement("canvas");
  canvas.width = sourceCanvas.width;
  canvas.height = sourceCanvas.height;
  const context = canvas.getContext("2d");
  if (!context) {
    return sourceCanvas;
  }
  const brightnessFactor = clampNumber(cell.targetBrightness / Math.max(photo.brightness || 1, 1), 0.58, cell.isTextPixel ? 1.55 : 1.18);
  const saturationFactor = clampNumber(cell.targetSaturation / Math.max(photo.saturation || 1, 1), 0.7, cell.isTextPixel ? 1.95 : 1.55);
  const hueRotate = clampNumber(normalizeHueRotation(cell.targetHue - photo.hue), cell.isTextPixel ? -42 : -18, cell.isTextPixel ? 42 : 18);
  const contrastFactor = cell.isTextPixel ? 1.16 : 1.06;

  context.filter = `brightness(${brightnessFactor}) saturate(${saturationFactor}) hue-rotate(${hueRotate}deg) contrast(${contrastFactor})`;
  context.drawImage(sourceCanvas, 0, 0, canvas.width, canvas.height);
  context.filter = "none";

  context.fillStyle = cell.isTextPixel ? "rgba(255, 223, 196, 0.09)" : "rgba(123, 36, 28, 0.22)";
  context.fillRect(0, 0, canvas.width, canvas.height);
  return canvas;
}

function drawIamAcuiteMask(context, width, height, tileSize) {
  context.clearRect(0, 0, width, height);
  context.fillStyle = "#000";
  context.fillRect(0, 0, width, height);
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillStyle = "#fff";

  const horizontalInset = tileSize || 0;
  const maxHeadlineWidth = width - (horizontalInset * 2);
  const acuiteSize = fitIamAcuiteTextSize(context, "Acuite", "900", maxHeadlineWidth, 360, 180);
  const iamSize = fitIamAcuiteTextSize(context, "I am", "700", maxHeadlineWidth * 0.36, 132, 84);

  context.font = `700 ${iamSize}px 'Avenir Next', 'Segoe UI', sans-serif`;
  context.fillText("I am", width / 2, height * 0.28);
  context.font = `900 ${acuiteSize}px 'Avenir Next', 'Segoe UI', sans-serif`;
  context.fillText("Acuite", width / 2, height * 0.62);
}

function clampNumber(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function clampHue(value) {
  return ((value % 360) + 360) % 360;
}

function circularHueDistance(left, right) {
  const difference = Math.abs(clampHue(left) - clampHue(right));
  return Math.min(difference, 360 - difference);
}

function normalizeHueRotation(value) {
  const normalized = ((value + 180) % 360 + 360) % 360 - 180;
  return normalized === -180 ? 180 : normalized;
}

function rangePenalty(value, min, max) {
  if (value < min) {
    return (min - value) * 1.4;
  }
  if (value > max) {
    return (value - max) * 1.4;
  }
  return 0;
}

function rangePenaltyHue(value, min, max) {
  const lowDistance = circularHueDistance(value, min);
  const highDistance = circularHueDistance(value, max);
  const targetDistance = circularHueDistance(min, max);
  const insideRange = lowDistance + highDistance <= targetDistance + 0.001;
  if (insideRange) {
    return 0;
  }
  return Math.min(lowDistance, highDistance) * 0.9;
}

function fitIamAcuiteTextSize(context, text, weight, maxWidth, startSize, minSize) {
  for (let size = startSize; size >= minSize; size -= 2) {
    context.font = `${weight} ${size}px 'Avenir Next', 'Segoe UI', sans-serif`;
    if (context.measureText(text).width <= maxWidth) {
      return size;
    }
  }
  return minSize;
}

async function prepareIamAcuiteTile(photoUrl) {
  const image = await loadImage(photoUrl);
  if (!image) {
    return null;
  }
  const sourceWidth = image.naturalWidth || image.width;
  const sourceHeight = image.naturalHeight || image.height;
  if (!sourceWidth || !sourceHeight) {
    return null;
  }
  const size = Math.min(sourceWidth, sourceHeight);
  const offsetX = Math.max(0, (sourceWidth - size) / 2);
  const offsetY = Math.max(0, (sourceHeight - size) / 2);
  const canvas = document.createElement("canvas");
  canvas.width = 72;
  canvas.height = 72;
  const context = canvas.getContext("2d");
  if (!context) {
    return null;
  }
  context.drawImage(image, offsetX, offsetY, size, size, 0, 0, canvas.width, canvas.height);
  const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
  let total = 0;
  let count = 0;
  let hueX = 0;
  let hueY = 0;
  let saturationTotal = 0;
  for (let index = 0; index < pixels.length; index += 16) {
    const red = pixels[index];
    const green = pixels[index + 1];
    const blue = pixels[index + 2];
    total += (red * 0.299) + (green * 0.587) + (blue * 0.114);
    const { hue, saturation } = rgbToHsl(red, green, blue);
    const hueWeight = Math.max(0.08, saturation);
    hueX += Math.cos(hue * Math.PI * 2) * hueWeight;
    hueY += Math.sin(hue * Math.PI * 2) * hueWeight;
    saturationTotal += saturation * 100;
    count += 1;
  }
  const averagedHue = hueX === 0 && hueY === 0
    ? 0
    : clampHue((Math.atan2(hueY, hueX) * 180) / Math.PI);
  return {
    id: `${photoUrl}:${count}`,
    canvas,
    brightness: count ? total / count : 0,
    hue: averagedHue,
    saturation: count ? saturationTotal / count : 0,
  };
}

function rgbToHsl(red, green, blue) {
  const r = red / 255;
  const g = green / 255;
  const b = blue / 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const lightness = (max + min) / 2;
  const delta = max - min;

  if (!delta) {
    return { hue: 0, saturation: 0, lightness };
  }

  const saturation = lightness > 0.5
    ? delta / (2 - max - min)
    : delta / (max + min);

  let hue;
  switch (max) {
    case r:
      hue = ((g - b) / delta) + (g < b ? 6 : 0);
      break;
    case g:
      hue = ((b - r) / delta) + 2;
      break;
    default:
      hue = ((r - g) / delta) + 4;
      break;
  }
  hue /= 6;

  return {
    hue,
    saturation,
    lightness,
  };
}

function loadImage(src) {
  return new Promise((resolve) => {
    const image = new Image();
    image.decoding = "async";
    image.onload = () => resolve(image);
    image.onerror = () => resolve(null);
    image.src = src;
  });
}

function signatureHash(value) {
  return String(value || "").split("").reduce((total, character) => {
    return (total + character.charCodeAt(0)) % 100000;
  }, 0);
}

function hashStringToUnit(value) {
  let hash = 2166136261;
  const input = String(value || "");
  for (let index = 0; index < input.length; index += 1) {
    hash ^= input.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return (hash >>> 0) / 4294967295;
}

function deterministicShuffle(items, seed) {
  return items
    .map((item, index) => ({
      item,
      order: signatureHash(`${seed}:${index}:${item.id || item.brightness || "tile"}`),
    }))
    .sort((left, right) => left.order - right.order)
    .map((entry) => entry.item);
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

function ordinalSuffix(value) {
  const day = Number(value);
  if (!Number.isFinite(day)) {
    return "";
  }
  const remainderHundred = day % 100;
  if (remainderHundred >= 11 && remainderHundred <= 13) {
    return "th";
  }
  switch (day % 10) {
    case 1:
      return "st";
    case 2:
      return "nd";
    case 3:
      return "rd";
    default:
      return "th";
  }
}

function formatAnnouncementLongDate(value) {
  if (!value) {
    return "";
  }
  const parsed = new Date(`${String(value).slice(0, 10)}T00:00:00`);
  if (Number.isNaN(parsed.getTime())) {
    return String(value);
  }
  const weekday = parsed.toLocaleDateString("en-IN", { weekday: "long" });
  const month = parsed.toLocaleDateString("en-IN", { month: "long" });
  const day = parsed.getDate();
  return `${weekday}, ${day}${ordinalSuffix(day)} ${month} ${parsed.getFullYear()}`;
}

function formatTownHallModeLabel(value) {
  const normalized = String(value || "").trim().toLowerCase();
  if (normalized === "in_person") {
    return "In Person";
  }
  if (normalized === "hybrid") {
    return "Hybrid";
  }
  if (normalized === "online") {
    return "Online";
  }
  return capitalize(normalized.replaceAll("_", " "));
}

function normalizeTownHallVenueLabel(value) {
  const trimmed = String(value || "").trim();
  if (!trimmed) {
    return "Venue: TBD";
  }
  if (/^venue\s*:/i.test(trimmed)) {
    return trimmed;
  }
  return `Venue: ${trimmed}`;
}

function getTownHallCountdownLabel(value) {
  if (!value) {
    return "";
  }
  const parsed = new Date(`${String(value).slice(0, 10)}T00:00:00`);
  if (Number.isNaN(parsed.getTime())) {
    return "";
  }
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const eventDay = new Date(parsed.getFullYear(), parsed.getMonth(), parsed.getDate());
  const difference = Math.round((eventDay.getTime() - today.getTime()) / 86400000);
  if (difference > 1) {
    return `${difference} days to go`;
  }
  if (difference === 1) {
    return "1 day to go";
  }
  if (difference === 0) {
    return "Today";
  }
  return "Completed";
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

function formatCeoDeskPostedDate(value) {
  if (!value) {
    return "";
  }
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return String(value);
  }
  return parsed.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

function formatMonthDay(value) {
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
  });
}

function formatHolidayLongDate(value) {
  if (!value) {
    return "";
  }
  const parsed = new Date(`${value}T00:00:00`);
  if (Number.isNaN(parsed.getTime())) {
    return String(value);
  }
  return parsed.toLocaleDateString("en-IN", {
    weekday: "long",
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function getUpcomingHolidayItems(daysAhead = 30) {
  const now = new Date();
  const todayStamp = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
  const endStamp = new Date(now.getFullYear(), now.getMonth(), now.getDate() + daysAhead).getTime();
  return COMPANY_HOLIDAY_CALENDAR
    .map((item) => ({
      ...item,
      parsedDate: new Date(`${item.date}T00:00:00`),
    }))
    .filter((item) => !Number.isNaN(item.parsedDate.getTime()))
    .filter((item) => item.parsedDate.getTime() >= todayStamp)
    .filter((item) => item.parsedDate.getTime() <= endStamp)
    .sort((left, right) => left.parsedDate.getTime() - right.parsedDate.getTime());
}

function renderSidebarHolidays() {
  const container = document.getElementById("sidebar-holidays-list");
  if (!container) {
    return;
  }

  const upcoming = getUpcomingHolidayItems();

  if (!upcoming.length) {
    container.innerHTML = '<div class="empty-state">No published holidays in the next 30 days.</div>';
    return;
  }

  container.className = "sidebar-holiday-list";
  container.innerHTML = upcoming.map((item) => `
    <article class="sidebar-holiday-item">
      <strong>${escapeHtml(item.label)}</strong>
      <span>${escapeHtml(formatMonthDay(item.date))}</span>
      <span>${escapeHtml(item.applicability || "")}</span>
    </article>
  `).join("");
}

function renderHolidayPanel() {
  const monthList = document.getElementById("holiday-month-list");
  const monthMeta = document.getElementById("holiday-month-meta");
  const fullList = document.getElementById("holiday-calendar-list");
  if (!monthList || !monthMeta || !fullList) {
    return;
  }

  const upcomingItems = getUpcomingHolidayItems();
  if (!upcomingItems.length) {
    monthMeta.textContent = "No published holidays fall in the next 30 days.";
    monthList.innerHTML = '<div class="empty-state">No published holidays in the next 30 days.</div>';
  } else {
    monthMeta.textContent = `${upcomingItems.length} holiday${upcomingItems.length === 1 ? "" : "s"} in the next 30 days.`;
    monthList.innerHTML = upcomingItems.map((item) => `
      <article class="holiday-card holiday-card-highlight">
        <p class="widget-kicker">${escapeHtml(formatMonthDay(item.date))}</p>
        <h3>${escapeHtml(item.label)}</h3>
        <div class="mini-item-meta">${escapeHtml(formatHolidayLongDate(item.date))}</div>
        <p>${escapeHtml(item.applicability || "All Offices")}</p>
      </article>
    `).join("");
  }

  fullList.innerHTML = COMPANY_HOLIDAY_CALENDAR.map((item) => `
    <article class="holiday-card">
      <div class="holiday-card-head">
        <div>
          <p class="widget-kicker">${escapeHtml(formatMonthDay(item.date))}</p>
          <h3>${escapeHtml(item.label)}</h3>
        </div>
        <span class="holiday-applicability">${escapeHtml(item.applicability || "All Offices")}</span>
      </div>
      <div class="mini-item-meta">${escapeHtml(formatHolidayLongDate(item.date))}</div>
    </article>
  `).join("");
}

function renderSidebarEvents() {
  const container = document.getElementById("sidebar-events-list");
  if (!container) {
    return;
  }

  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  const todayStamp = new Date(year, month, now.getDate()).getTime();
  const upcoming = COMPANY_EVENT_CALENDAR
    .map((item) => ({
      ...item,
      parsedDate: new Date(`${item.date}T00:00:00`),
    }))
    .filter((item) => !Number.isNaN(item.parsedDate.getTime()))
    .filter((item) => item.parsedDate.getFullYear() === year && item.parsedDate.getMonth() === month)
    .filter((item) => item.parsedDate.getTime() >= todayStamp)
    .sort((left, right) => left.parsedDate.getTime() - right.parsedDate.getTime());

  if (!upcoming.length) {
    container.innerHTML = '<div class="empty-state">No more published events this month.</div>';
    return;
  }

  container.className = "sidebar-holiday-list";
  container.innerHTML = upcoming.map((item) => `
    <article class="sidebar-holiday-item">
      <strong>${escapeHtml(item.label)}</strong>
      <span>${escapeHtml(formatMonthDay(item.date))}</span>
    </article>
  `).join("");
}

function syncFilterButtons() {
  const filterMap = {
    store: state.storeFilter,
    bulletin: state.bulletinFilter,
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
  applyTheme();
  renderPanels();
}

function applyTheme() {
  document.documentElement.setAttribute("data-theme", state.theme);
  document.querySelectorAll(".connect-brand-logo[data-light-src][data-dark-src]").forEach((logo) => {
    const targetSrc = state.theme === "dark" ? logo.dataset.darkSrc : logo.dataset.lightSrc;
    if (logo.getAttribute("src") !== targetSrc) {
      logo.setAttribute("src", targetSrc);
    }
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
  switchTab("profile");
}

function closeProfileBuilder() {
  switchTab("home");
}

function mapDirectoryProfileToCard(profile) {
  const company = profile.company_name || "";
  const companyLabel = displayCompanyName(company);
  const department = profile.department || "";
  const departmentForConnect = profile.department_for_connect || "";
  const functionName = profile.function_name || "";
  const office = profile.office_location || profile.location || profile.city || "";
  const branchLocation = profile.branch_location || profile.city || profile.location || office;
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
    branchLocation,
    officeLine: [office, companyLabel].filter(Boolean).join(" | "),
    employeeCode: profile.employee_code || "",
    coinBalance: String(profile.coin_balance?.available_points || 0),
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
      branchLocation,
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
  if (profileBuilderDraft.skills.length >= 3) {
    showToast("You can select up to 3 skills.");
    return;
  }
  profileBuilderDraft.skills = [...profileBuilderDraft.skills, skill];
  renderProfileBuilder();
}

function toggleProfileHobby(hobby) {
  if (!hobby) {
    return;
  }
  if (profileBuilderDraft.hobbies.includes(hobby)) {
    profileBuilderDraft.hobbies = profileBuilderDraft.hobbies.filter((item) => item !== hobby);
    renderProfileBuilder();
    return;
  }
  if (profileBuilderDraft.hobbies.length >= 3) {
    showToast("You can select up to 3 hobbies.");
    return;
  }
  profileBuilderDraft.hobbies = [...profileBuilderDraft.hobbies, hobby];
  renderProfileBuilder();
}

async function clearProfilePhoto(index) {
  if (Number.isNaN(index) || index < 0 || index > 1) {
    return;
  }
  if (!profileBuilderDraft.photos[index]) {
    return;
  }
  const confirmed = window.confirm("Delete this photo?");
  if (!confirmed) {
    return;
  }
  profileBuilderDraft.photos[index] = "";
  renderProfileBuilder();
  await saveProfileBuilder();
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
        hobbies: profileBuilderDraft.hobbies,
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
    if (appData.communityClubs.length || state.activeTab === "community") {
      await loadCommunityData();
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

function renderBulletinPostCard(post) {
  const showSupplementaryText = !post.bulletinCard;
  return `
    <article class="card voice-card bulletin-card bulletin-category-${escapeHtml(post.category)}" id="${post.id}">
      <div class="card-header">
        <div class="card-avatar" style="background:${gradientValue(post.avatar)}">${escapeHtml(post.initials)}</div>
        <div class="card-meta">
          <div class="card-name">${escapeHtml(post.authorName)}</div>
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
      ${
        showSupplementaryText
          ? `<div class="card-body">
              <div class="card-title">${escapeHtml(post.title)}</div>
              ${
                post.metaLines.length
                  ? `<div class="bulletin-meta-lines">
                      ${post.metaLines.map((line) => `<span class="mini-chip">${escapeHtml(line)}</span>`).join("")}
                    </div>`
                  : ""
              }
              ${post.body.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("")}
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
        ${renderDeleteLivePostButton(post, post.module || FEED_MODULE_BULLETIN)}
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

  if (postPayload.module === FEED_MODULE_BULLETIN) {
    const mapped = mapBulletinPost(postPayload);
    if (mapped.bulletinChannel === "ceo_desk") {
      appData.ceoDeskPosts = sortBulletinPostsNewestFirst(replaceMappedPost(appData.ceoDeskPosts, mapped));
      ceoDeskCachedAt = new Date().toISOString();
      ceoDeskShowingCachedData = false;
      saveCeoDeskCache();
      return;
    }
    if (mapped.homeAnnouncementTag || mapped.bulletinChannel === "announcements") {
      appData.homeAnnouncementPosts = sortBulletinPostsNewestFirst(
        replaceMappedPost(appData.homeAnnouncementPosts, mapped),
      );
      return;
    }
    if (isCelebrationBulletinPost(mapped)) {
      const existingIndex = appData.bulletinPosts.findIndex((item) => item.sourceId === mapped.sourceId);
      if (existingIndex >= 0) {
        appData.bulletinPosts.splice(existingIndex, 1, mapped);
      } else {
        appData.bulletinPosts.unshift(mapped);
      }
      appData.bulletinPosts = sortBulletinPostsNewestFirst(appData.bulletinPosts);
      return;
    }
    return;
  }

  if (postPayload.module === FEED_MODULE_EMPLOYEE_POSTS) {
    const mapped = mapMyPostSubmission(postPayload);
    appData.myPosts = replaceMappedPost(appData.myPosts, mapped);
    if (
      String(postPayload.topic || "").trim() === "employee_submission"
      && String(postPayload.moderation_status || "").trim() === "published"
      && Boolean(postPayload.metadata?.user_submission)
    ) {
      const bulletinMapped = mapBulletinPost(postPayload);
      const existingIndex = appData.bulletinPosts.findIndex((item) => item.sourceId === bulletinMapped.sourceId);
      if (existingIndex >= 0) {
        appData.bulletinPosts.splice(existingIndex, 1, bulletinMapped);
      } else {
        appData.bulletinPosts.unshift(bulletinMapped);
      }
      appData.bulletinPosts = sortBulletinPostsNewestFirst(appData.bulletinPosts);
    }
    return;
  }

  if (postPayload.module === FEED_MODULE_COMMUNITY) {
    const mapped = mapCommunityPost(postPayload);
    const existingItems = Array.isArray(appData.communityPostsByClub[mapped.clubKey])
      ? appData.communityPostsByClub[mapped.clubKey]
      : [];
    const existingIndex = existingItems.findIndex((item) => item.sourceId === mapped.sourceId);
    const nextItems = existingIndex >= 0
      ? existingItems.map((item) => (item.sourceId === mapped.sourceId ? mapped : item))
      : [mapped, ...existingItems];
    appData.communityPostsByClub[mapped.clubKey] = sortBulletinPostsNewestFirst(nextItems);
  }
}

function likeIcon() {
  return `
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017a2 2 0 01-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095a.905.905 0 00-.905.905c0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"></path>
    </svg>
  `;
}

function heartIcon() {
  return `
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
    </svg>
  `;
}

function isCelebrationBulletinPost(post) {
  return CELEBRATION_TEMPLATE_KEYS.has(String(post?.templateKey || "").trim());
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
