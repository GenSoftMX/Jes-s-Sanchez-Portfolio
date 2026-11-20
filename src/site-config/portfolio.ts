export interface LocalizedString {
  es: string;
  en: string;
}

export interface RoleItem {
  id: string;
  symbol: string;
  company: string;
  title: string;
  date: LocalizedString;
  mini: LocalizedString;
  summary: LocalizedString;
  points: {
    es: string[];
    en: string[];
  };
  note?: LocalizedString;
  link?: {
    label: string;
    url: string;
  };
  tags: string[];
}

export interface ProjectModalLink {
  url: string;
  es: string;
  en: string;
}

export interface ProjectItem {
  title: string;
  eyebrow: string;
  lead: LocalizedString;
  problem: LocalizedString;
  approach: LocalizedString;
  status: LocalizedString;
  links: ProjectModalLink[];
}

export const phrases = {
  "es": {
    "navHome": "Inicio",
    "navProjects": "Proyectos",
    "navCareer": "Experiencia",
    "navPaper": "Publicaciones",
    "navAbout": "Sobre mí",
    "contact": "Contacto",
    "heroEyebrow": "Hola, soy",
    "heroRole": "Ingeniero móvil en Enersí",
    "heroFocus": "Arquitectura de software · IA aplicada",
    "heroDescription": "Ingeniero de software especializado en desarrollo móvil y modernización de aplicaciones. Diseño soluciones para operaciones reales y exploro cómo la arquitectura y los agentes de IA pueden mejorar la forma en que construimos software.",
    "viewCareer": "Ver mi trayectoria",
    "viewProjects": "Explorar proyectos",
    "since2016": "Experiencia profesional desde 2016",
    "openResearch": "Open source e investigación",
    "specialtyMobile": "Ingeniería móvil",
    "specialtyArchitecture": "Arquitectura de software",
    "specialtyAI": "IA aplicada",
    "specialtyTools": "Herramientas para desarrolladores",
    "specialtyMobileDetail": "Flutter · Android · Kotlin · iOS",
    "specialtyArchitectureDetail": "Diseño · Refactorización · Calidad",
    "specialtyAIDetail": "Contexto · Ingeniería de prompts",
    "specialtyToolsDetail": "Open source · Integraciones",
    "photoPlaceholder": "Espacio para fotografía real",
    "photoLabel": "Foto profesional",
    "photoHint": "Cambia esta vista con tu imagen",
    "uploadPhoto": "Añadir mi fotografía",
    "workLabel": "Ingeniería e investigación",
    "workTitle": "Proyectos destacados",
    "workIntro": "Proyectos personales y open source, diferenciados de mi trabajo profesional para las empresas.",
    "viewPublication": "Ver publicación ↗",
    "vostokShort": "Flujo guiado para desarrollar con agentes de IA mediante contexto progresivo, evidencia verificable y aprobación humana.",
    "jintentShort": "Biblioteca Flutter de código abierto para modelar intents, estado inmutable y efectos de interfaz de forma explícita.",
    "supportShort": "Proyecto independiente de triage técnico asistido por IA, análisis de repositorios y asignación contextual de incidencias.",
    "lakamShort": "Propuesta para conectar redes sociales, programar publicaciones y recomendar contenido con IA a partir de estadísticas.",
    "exploreProject": "Ver caso de estudio",
    "projectEthicsTitle": "Proyectos propios y experiencia profesional son cosas distintas.",
    "projectEthicsCopy": "Support Triage AI es un prototipo independiente y proyecto personal. No está vinculado a empleadores ni se muestran sistemas internos o código propietario.",
    "knowMore": "Conocer más",
    "careerLabel": "Mi recorrido profesional",
    "careerTitle": "Experiencia y evolución",
    "careerIntro": "Selecciona una posición para explorar proyectos y contribuciones reales a lo largo de mi carrera.",
    "researchLabel": "Publicaciones · Investigación",
    "researchTitle": "La ingeniería también se documenta.",
    "researchIntro": "Ideas, arquitectura y prácticas para integrar agentes de IA en el desarrollo de software de forma verificable.",
    "paperDescription": "Whitepaper sobre ingeniería de software asistida por agentes: selección progresiva de contexto, especificaciones, ejecución controlada, evidencia y participación humana en decisiones críticas. Publicado en Zenodo el 19 de noviembre de 2026.",
    "readPaper": "Consultar publicación",
    "allVersions": "DOI de todas las versiones",
    "skillsLabel": "Experiencia técnica",
    "skillsTitle": "Tecnologías y áreas de enfoque",
    "skillsIntro": "Una base sólida en desarrollo empresarial y móvil, complementada con arquitectura, herramientas para desarrolladores e IA.",
    "skills1": "Desarrollo móvil",
    "skills1desc": "Aplicaciones para clientes y operadores, modernización, arquitectura offline y operaciones en campo.",
    "skills2": "Arquitectura y calidad",
    "skills2desc": "Refactorización, separación de responsabilidades, integración de sistemas y prácticas de ingeniería verificables.",
    "skills3": "IA aplicada",
    "skills3desc": "Sistemas con agentes, ingeniería de contexto, flujos de trabajo, trazabilidad y supervisión humana.",
    "skills4": "Backend e integraciones",
    "skills4desc": "Experiencia previa en sistemas empresariales, servicios, bases de datos y automatización.",
    "aboutLabel": "Sobre mí",
    "aboutTitle": "Software que funciona en el mundo real.",
    "aboutQuote": "“Me interesa tanto cómo construimos un sistema como nuestra capacidad de mantenerlo, verificarlo y mejorarlo.”",
    "aboutP1": "Soy Jesús Sánchez, ingeniero de software con trayectoria desde 2016. He trabajado en sistemas empresariales, arquitectura, aplicaciones móviles para operaciones y clientes, y modernización tecnológica.",
    "aboutP2": "Actualmente me desempeño como Mobile Engineer en Enersí. En paralelo, desarrollo herramientas open source y publico investigación sobre flujos de trabajo y arquitectura de agentes de IA para la ingeniería de software.",
    "educationHeading": "Formación académica",
    "educationText": "Ingeniería en Sistemas Computacionales · Instituto Tecnológico Superior de Guasave (2015).",
    "contactOverline": "Contacto y colaboración",
    "contactHeading": "¿Construimos algo juntos?",
    "contactText": "Abierto a conversaciones sobre ingeniería móvil, arquitectura, IA aplicada, investigación y oportunidades profesionales.",
    "contactEmail": "Enviar email ↗",
    "contactGithub": "Ver GitHub ↗",
    "contactLinkedIn": "Ver LinkedIn ↗",
    "themeToDark": "Cambiar a tema oscuro",
    "themeToLight": "Cambiar a tema claro",
    "footerNote": "Mobile Engineering · Software Architecture · AI Agents",
    "rights": "Todos los derechos reservados."
  },
  "en": {
    "navHome": "Home",
    "navProjects": "Projects",
    "navCareer": "Experience",
    "navPaper": "Publications",
    "navAbout": "About",
    "contact": "Contact",
    "heroEyebrow": "Hi, I am",
    "heroRole": "Mobile Engineer at Enersí",
    "heroFocus": "Software architecture · Applied AI",
    "heroDescription": "Software engineer specializing in mobile development and application modernization. I build solutions for real-world operations and explore how architecture and AI agents can improve software engineering.",
    "viewCareer": "Explore experience",
    "viewProjects": "Explore projects",
    "since2016": "Software engineering career since 2016",
    "openResearch": "Open source & research",
    "specialtyMobile": "Mobile engineering",
    "specialtyArchitecture": "Software architecture",
    "specialtyAI": "Applied AI",
    "specialtyTools": "Developer tools",
    "specialtyMobileDetail": "Flutter · Android · Kotlin · iOS",
    "specialtyArchitectureDetail": "Design · Refactoring · Quality",
    "specialtyAIDetail": "Context engineering · Prompt engineering",
    "specialtyToolsDetail": "Open source · Integrations",
    "photoPlaceholder": "Your real portrait goes here",
    "photoLabel": "Professional photo",
    "photoHint": "Replace this placeholder with your photo",
    "uploadPhoto": "Add my photo",
    "workLabel": "Engineering & research",
    "workTitle": "Selected projects",
    "workIntro": "Personal and open-source projects, clearly separated from my work for employers.",
    "viewPublication": "View publication ↗",
    "vostokShort": "Guided AI-agent development workflow using progressive context, verifiable evidence and human approval.",
    "jintentShort": "Open-source Flutter library for explicit intents, immutable state and one-time UI effects.",
    "supportShort": "Independent AI-assisted technical triage prototype with repository analysis and context-based incident routing.",
    "lakamShort": "Concept for connecting social networks, scheduling posts and using analytics to recommend content with AI.",
    "exploreProject": "Read case study",
    "projectEthicsTitle": "Personal projects and employer experience are separate.",
    "projectEthicsCopy": "Support Triage AI is an independent prototype and personal project. It is not affiliated with employers, and discloses no proprietary code or internal systems.",
    "knowMore": "Learn more",
    "careerLabel": "Professional journey",
    "careerTitle": "Experience & growth",
    "careerIntro": "Select a role to explore projects and actual contributions throughout my career.",
    "researchLabel": "Publications · Research",
    "researchTitle": "Engineering should be documented.",
    "researchIntro": "Architecture and practices for integrating AI agents into verifiable software development.",
    "paperDescription": "Whitepaper on agent-assisted software engineering: progressive context selection, specifications, controlled execution, evidence and human oversight in critical decisions. Published on Zenodo on November 19, 2026.",
    "readPaper": "View publication",
    "allVersions": "All-versions DOI",
    "skillsLabel": "Technical background",
    "skillsTitle": "Expertise & technologies",
    "skillsIntro": "A strong foundation in enterprise and mobile development, complemented by architecture, developer tools and AI.",
    "skills1": "Mobile development",
    "skills1desc": "Customer and operator applications, modernization, offline behavior and field operations.",
    "skills2": "Architecture & quality",
    "skills2desc": "Refactoring, separation of concerns, system integration and verifiable engineering practices.",
    "skills3": "Applied AI",
    "skills3desc": "Agentic systems, context engineering, workflows, traceability and human oversight.",
    "skills4": "Backend & integrations",
    "skills4desc": "Experience in enterprise systems, services, databases and automation.",
    "aboutLabel": "About",
    "aboutTitle": "Software that works in the real world.",
    "aboutQuote": "“I care as much about how a system is built as our ability to maintain, verify and improve it.”",
    "aboutP1": "I’m Jesús Sánchez, a software engineer whose professional career began in 2016. I have worked on enterprise systems, architecture, mobile applications for field operations and customers, and technology modernization.",
    "aboutP2": "I currently work as a Mobile Engineer at Enersí. In parallel, I develop open-source tools and publish research on AI-agent workflows and architecture for software engineering.",
    "educationHeading": "Education",
    "educationText": "Computer Systems degree · Instituto Tecnológico Superior de Guasave (2015).",
    "contactOverline": "Contact & collaboration",
    "contactHeading": "Shall we build something?",
    "contactText": "Open to conversations about mobile engineering, architecture, applied AI, research and professional opportunities.",
    "contactEmail": "Send email ↗",
    "contactGithub": "View GitHub ↗",
    "contactLinkedIn": "View LinkedIn ↗",
    "themeToDark": "Switch to dark theme",
    "themeToLight": "Switch to light theme",
    "footerNote": "Mobile Engineering · Software Architecture · AI Agents",
    "rights": "All rights reserved."
  }
} as const;

export const roles: RoleItem[] = [
  {
    "id": "enersi",
    "symbol": "E",
    "company": "Enersí",
    "title": "Mobile Engineer",
    "date": {
      "es": "2025 – Actualidad",
      "en": "2025 – Present"
    },
    "mini": {
      "es": "Operaciones, backend y logística",
      "en": "Operations, backend & logistics"
    },
    "summary": {
      "es": "Desarrollo de aplicaciones móviles para la distribución de gas en México, conectando operaciones en campo, estaciones de servicio, aplicaciones de clientes y operadores.",
      "en": "Mobile applications for gas distribution across Mexico, spanning field operations, service stations, customer apps and operator workflows."
    },
    "points": {
      "es": [
        "Aplicaciones para pipas, recursos de reparto y operaciones de venta o entrega de gas.",
        "Administración de estaciones y procesos de inicio y cierre de rutas de venta.",
        "App de cliente: pedidos a domicilio, direcciones, pagos y mapas.",
        "App de operador: notificaciones push, pedidos asignados, navegación y recorridos.",
        "Participación en modernización de aplicativos legacy y evolución de soluciones móviles.",
        "Colaboración en tareas de backend."
      ],
      "en": [
        "Apps for distribution trucks, delivery personnel and sales/delivery operations.",
        "Service-station management, sales-route start and completion workflows.",
        "Customer app: home-delivery orders, addresses, payments and maps.",
        "Operator app: push notifications, assigned orders, navigation and routes.",
        "Participation in legacy application modernization and mobile-platform evolution.",
        "Contribute to backend work."
      ]
    },
    "tags": [
      "Mobile Engineering",
      "Logistics",
      "Android",
      "Kotlin",
      "Backend"
    ]
  },
  {
    "id": "wadi",
    "symbol": "W",
    "company": "Wadi",
    "title": "Mobile Engineer",
    "date": {
      "es": "2023",
      "en": "2023"
    },
    "mini": {
      "es": "Flutter · Refactoring · Offline-first",
      "en": "Flutter · Refactoring · Offline-first"
    },
    "summary": {
      "es": "Desarrollo de aplicaciones para clientes y operadores de distribución de gas. Lideré una refactorización integral de la app de operador en Flutter, con foco en evolución arquitectónica y conectividad limitada.",
      "en": "Customer and operator apps for gas distribution. I carried out a full Flutter operator-app refactor, focusing on architecture and limited-connectivity use cases."
    },
    "points": {
      "es": [
        "Refactorización completa de la aplicación de operador desarrollada en Flutter.",
        "Implementación de funcionalidad offline para operaciones con conectividad limitada.",
        "Integración de chat en tiempo real entre operadores y equipo de soporte.",
        "Desarrollo de un módulo de check-in para operadores.",
        "Contribuciones en la aplicación de clientes para pedidos de gas.",
        "Evolución de la arquitectura existente basada en Riverpod."
      ],
      "en": [
        "Full refactor of the Flutter operator application.",
        "Offline functionality for workflows with limited connectivity.",
        "Real-time chat integration between operators and support.",
        "Operator check-in module.",
        "Contributions to the customer gas-ordering app.",
        "Evolution of the existing Riverpod-based architecture."
      ]
    },
    "note": {
      "es": "Aquí surgió la necesidad que dio origen a JIntent: abstraer y mejorar el manejo de interacciones dentro de Flutter. La herramienta evolucionó después como una iniciativa independiente.",
      "en": "The need that sparked JIntent emerged here: improving how Flutter interactions are modeled. The tool later evolved into an independent initiative."
    },
    "tags": [
      "Flutter",
      "Dart",
      "Riverpod",
      "Offline-first",
      "JIntent"
    ],
    "link": {
      "label": "JIntent",
      "url": "https://pub.dev/packages/jintent"
    }
  },
  {
    "id": "hlc",
    "symbol": "H",
    "company": "High Level Capital",
    "title": "Senior Software Engineer",
    "date": {
      "es": "Desde abr. 2020",
      "en": "Since Apr 2020"
    },
    "mini": {
      "es": "Aplicaciones y servicios empresariales",
      "en": "Business apps & services"
    },
    "summary": {
      "es": "Desarrollo de soluciones móviles y servicios empresariales, con trabajo de integración backend y servicios en la nube.",
      "en": "Development of mobile solutions and business services, with backend and cloud integration work."
    },
    "points": {
      "es": [
        "Desarrollo de soluciones móviles y servicios backend.",
        "Trabajo con servicios AWS y despliegues cloud.",
        "Participación en integraciones, herramientas empresariales y mantenimiento de sistemas."
      ],
      "en": [
        "Mobile and backend service development.",
        "AWS cloud services and deployment workflows.",
        "Contributions to business integrations, internal tools and maintenance."
      ]
    },
    "tags": [
      "AWS",
      "Backend",
      "Mobile"
    ]
  },
  {
    "id": "ucall",
    "symbol": "U",
    "company": "Ucall",
    "title": "Full Stack Developer",
    "date": {
      "es": "Mar. – oct. 2019",
      "en": "Mar – Oct 2019"
    },
    "mini": {
      "es": "Call center · C# · Auditoría",
      "en": "Call center · C# · Audit"
    },
    "summary": {
      "es": "Desarrollo de un sistema de call center en C# con asignación automática de llamadas según la evaluación y especialización de los agentes, más herramientas de auditoría para supervisores.",
      "en": "Built a C# call-center system with automatic call routing based on agents’ ratings and specialties, plus auditing tools for managers."
    },
    "points": {
      "es": [
        "Aplicación de escritorio con C# y WPF para la operación del call center.",
        "Enrutamiento automático de llamadas a agentes según especialización y calificación.",
        "Grabación y almacenamiento de llamadas en infraestructura cloud.",
        "Transcripciones, revisión de incidencias y consulta de grabaciones para supervisión."
      ],
      "en": [
        "C# / WPF desktop app for call-center operations.",
        "Automatic call routing using agent specialization and ratings.",
        "Call recording and cloud storage.",
        "Transcripts, incident reviews and recorded-call access for supervisors."
      ]
    },
    "tags": [
      "C#",
      "WPF",
      "Azure",
      "Automation"
    ]
  },
  {
    "id": "samsum",
    "symbol": "S",
    "company": "Samsum Contractor",
    "title": "Software Developer",
    "date": {
      "es": "Ene. 2019 – abr. 2023",
      "en": "Jan 2019 – Apr 2023"
    },
    "mini": {
      "es": "Mantenimiento, pruebas y documentación",
      "en": "Maintenance, testing & docs"
    },
    "summary": {
      "es": "Mantenimiento y mejora de una aplicación empresarial, corrigiendo incidencias en el cliente, los servicios y la base de datos.",
      "en": "Maintained and improved a business application, fixing defects across frontend, services and database."
    },
    "points": {
      "es": [
        "Corrección de errores en frontend y backend.",
        "Mantenimiento de datos y servicios empresariales.",
        "Elaboración de documentación técnica y ejecución de pruebas."
      ],
      "en": [
        "Frontend and backend bug fixes.",
        "Maintenance of business services and data.",
        "Technical documentation and application testing."
      ]
    },
    "tags": [
      "Angular",
      "Backend",
      "Testing"
    ]
  },
  {
    "id": "coppelA",
    "symbol": "C",
    "company": "Coppel",
    "title": "Software Architect",
    "date": {
      "es": "Ene. – dic. 2018",
      "en": "Jan – Dec 2018"
    },
    "mini": {
      "es": "Arquitectura, estándares y optimización",
      "en": "Architecture, standards & optimization"
    },
    "summary": {
      "es": "Participé en iniciativas de arquitectura, análisis de software y definición de formas de trabajo. Fui integrante del comité de optimización de código y colaboré en la adopción temprana de tecnologías web.",
      "en": "Worked on architecture, software analysis and engineering standards. Joined the code-optimization committee and supported the early adoption of new web technologies."
    },
    "points": {
      "es": [
        "Participación en comité de optimización de código y estandarización de prácticas de desarrollo.",
        "Contribuciones a sesiones de definición de procesos y formas de trabajo.",
        "Propuesta y adopción temprana de Angular; capacitación a otros equipos.",
        "Investigación y optimización de procesos críticos sobre SQL Server.",
        "Análisis de requisitos y viabilidad de soluciones técnicas."
      ],
      "en": [
        "Member of a code-optimization committee and engineering standards initiatives.",
        "Participation in defining team processes and engineering practices.",
        "Early Angular advocacy and adoption; training across teams.",
        "Research and optimization of critical SQL Server processes.",
        "Requirements analysis and technical feasibility."
      ]
    },
    "tags": [
      "Architecture",
      "Angular",
      "SQL Server",
      "Standards"
    ]
  },
  {
    "id": "coppelD",
    "symbol": "C",
    "company": "Coppel",
    "title": "Software Developer",
    "date": {
      "es": "Ene. 2016 – dic. 2017",
      "en": "Jan 2016 – Dec 2017"
    },
    "mini": {
      "es": "Sistemas empresariales · Angular",
      "en": "Enterprise systems · Angular"
    },
    "summary": {
      "es": "Desarrollo de aplicaciones empresariales para análisis comercial y operaciones internas, incluyendo sistemas de información de ventas y adopción temprana de Angular.",
      "en": "Developed enterprise applications for business analytics and internal operations, including sales reporting systems and early Angular applications."
    },
    "points": {
      "es": [
        "Sistema de análisis de ventas por departamento, clase y familia.",
        "Desarrollo con C#, PostgreSQL y servicios PHP.",
        "Participación temprana en aplicaciones Angular 2, modularización y prácticas de revisión de código.",
        "Documentación técnica y participación en pruebas."
      ],
      "en": [
        "Sales analysis system by department, class and product family.",
        "Development using C#, PostgreSQL and PHP services.",
        "Early Angular 2 implementation, modularization and code reviews.",
        "Technical documentation and testing."
      ]
    },
    "tags": [
      "C#",
      "PostgreSQL",
      "Angular",
      "PHP"
    ]
  }
];

export const projects: Record<string, ProjectItem> = {
  "vostok": {
    "title": "Vostok AI Workflow",
    "eyebrow": "AI ENGINEERING · WORKFLOW",
    "lead": {
      "es": "Iniciativa de ingeniería abierta para guiar el desarrollo asistido por agentes de IA.",
      "en": "Open engineering initiative to guide agent-assisted software development."
    },
    "problem": {
      "es": "Desarrollar con agentes de IA exige límites de alcance, selección de contexto y evidencia verificable, no solo producir cambios de código.",
      "en": "AI-assisted development requires boundaries, curated context and verifiable evidence, not merely code generation."
    },
    "approach": {
      "es": "Diseñé un flujo que combina especificaciones, selección progresiva de contexto, ejecución controlada y verificación basada en evidencia, con aprobación humana en decisiones críticas.",
      "en": "I designed a workflow combining specifications, progressive context selection, controlled execution and evidence-based verification, with human approval for critical decisions."
    },
    "status": {
      "es": "La investigación está publicada en Zenodo; el flujo de trabajo sigue en desarrollo y su implementación no se comparte aquí.",
      "en": "The research is published on Zenodo; the workflow remains in development and its implementation is not shared here."
    },
    "links": [
      {
        "es": "Leer whitepaper",
        "en": "Read whitepaper",
        "url": "https://doi.org/10.5281/zenodo.24361807"
      }
    ]
  },
  "jintent": {
    "title": "JIntent",
    "eyebrow": "FLUTTER · DEVELOPER TOOLING",
    "lead": {
      "es": "Una herramienta de arquitectura de Flutter cuya motivación surgió de necesidades de refactorización en Wadi.",
      "en": "A Flutter architecture tool motivated by refactoring needs encountered at Wadi."
    },
    "problem": {
      "es": "En una aplicación real construida con Riverpod surgió la necesidad de organizar mejor las interacciones y dar soporte a una evolución profunda de la arquitectura.",
      "en": "A real application built with Riverpod needed better interaction modeling while undergoing major architectural evolution."
    },
    "approach": {
      "es": "Extraje esa necesidad de modelado de interacciones y desarrollé JIntent como una biblioteca Flutter independiente: las acciones se expresan como intents, el estado es inmutable y los efectos de UI se manejan fuera del estado persistente.",
      "en": "I extracted that interaction-modeling need and developed JIntent as an independent Flutter library: actions are expressed as intents, state is immutable, and UI effects are handled outside persistent state."
    },
    "status": {
      "es": "Paquete open source publicado en pub.dev. La relación con Wadi explica el origen del problema, no una publicación de código propietario del empleador.",
      "en": "Open-source package published on pub.dev. Wadi provides the problem context; no employer-owned code is represented as part of the package."
    },
    "links": [
      {
        "es": "Paquete JIntent",
        "en": "JIntent package",
        "url": "https://pub.dev/packages/jintent"
      },
      {
        "es": "Repositorio en GitHub",
        "en": "GitHub repository",
        "url": "https://github.com/GenSoftMX/JIntent"
      }
    ]
  },
  "support": {
    "title": "Support Triage AI",
    "eyebrow": "AGENTIC SUPPORT · INDEPENDENT",
    "lead": {
      "es": "Prueba de concepto independiente para automatizar triage técnico y analizar incidencias con agentes de IA.",
      "en": "Independent proof of concept for automated technical triage and agent-assisted incident analysis."
    },
    "problem": {
      "es": "Clasificar tickets, recopilar contexto y asignar responsables requiere conectar información de incidencias, repositorios y equipos.",
      "en": "Classifying tickets, gathering context and assigning owners requires information across incidents, repositories and engineering teams."
    },
    "approach": {
      "es": "Arquitectura orientada a análisis de repositorios, enriquecimiento de contexto, triage, enrutamiento y conectores de Jira y Slack.",
      "en": "Architecture for repository analysis, context enrichment, triage, routing and Jira/Slack connectors."
    },
    "status": {
      "es": "Prototipo personal e investigación independiente. Las integraciones y capacidades no se presentan como completamente terminadas.",
      "en": "Personal prototype and independent research. Integrations and capabilities are not claimed to be fully complete."
    },
    "links": [
      {
        "es": "Repositorio público",
        "en": "Public repository",
        "url": "https://github.com/GenSoftMX/Support-Triage-AI"
      }
    ]
  },
  "lakam": {
    "title": "Lakam Flow",
    "eyebrow": "PRODUCT CONCEPT · SOCIAL TOOLS",
    "lead": {
      "es": "Plataforma en diseño para administración y programación de publicaciones en distintas redes sociales.",
      "en": "Product concept to manage and schedule posts across social platforms."
    },
    "problem": {
      "es": "Programar contenido en varias redes y tomar decisiones a partir de sus métricas suele requerir tareas repetitivas y análisis manual.",
      "en": "Cross-platform scheduling and interpreting channel performance often involves repetitive tasks and manual analysis."
    },
    "approach": {
      "es": "Primer alcance: conectar cuentas autorizadas, programar publicaciones, consultar estadísticas disponibles y sugerir contenido diario según la respuesta de la audiencia.",
      "en": "Initial scope: connect authorized accounts, schedule posts, review accessible analytics and suggest daily content based on audience response."
    },
    "status": {
      "es": "Producto en desarrollo. La generación multimedia queda explícitamente fuera de este primer alcance.",
      "en": "In development. Multimedia generation is explicitly out of scope for the initial product."
    },
    "links": []
  }
};
