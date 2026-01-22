#import "@preview/touying:0.5.3": *
#import themes.metropolis: *

// Setup the theme
#show: metropolis-theme.with(
  aspect-ratio: "16-9",
  config-info: (
    title: [Weather AI Analytics],
    subtitle: [Localized Forecasting via SLR and EWMA],
    author: [Artsiom Hancharenka, Nil Dvorakovskiy],
    date: datetime.today().display(),
  ),
)

#slide()[
  #align(center + horizon)[
    #text(size: 3em, weight: "bold", style: "italic")[Weather AI Analytics]
    #v(0.5em)
    #text(size: 1.4em, weight: "bold")[A Localized Forecasting Solution \ for SLR and EWMA Models]
  ]

  #place(bottom + right, dx: -8%)[
    #set text(size: 0.8em, weight: "medium")
    #align(right)[
      By Artsiom Hancharenka \
      Nil Dvorakovskiy \
      #datetime.today().display()
    ]
  ]
]

== Table of contents
#outline(title: none, indent: 1em, depth: 2)

== Motivation
- *Global Context:* Demand for precise, localized weather information has never been higher.
- *The Problem:* Domination of resource-heavy Numerical Weather Prediction (NWP) models.
- *Objective:* Create a lightweight, computationally efficient solution that works on the edge.

== Aim: Theory Verification via Web Platform
Instead of relying on theoretical simulations, we developed a full-stack web application to:
- *Check and Prove:* Validate Simple Linear Regression (SLR) and Exponentially Weighted Moving Average (EWMA) against real-world data.
- *Live Testing:* Compare AI predictions with actual meteorological outcomes in real-time.
- *Accessibility:* Provide a user-friendly interface for localized analytics.

== Theoretical Foundation
The study addresses distinct temporal behaviors based on two scientific pillars:
- *Persistence and Momentum Theory:* Using SLR to capture stable temperature trends.
- *Chaotic Volatility:* Using EWMA to handle rapid, localized fluctuations (e.g., humidity).

== Practical Usage: 8-Bit Optimization
Our algorithms are designed with extreme efficiency in mind:
- *Low-Power Deployment:* Well-optimized for **8-bit microcomputers** and embedded systems.
- *Smart Hardware:* Ideal for embedding directly into digital thermometers and standalone weather stations.
- *No Heavy Math:* Relies on simple arithmetic, removing the need for high-end floating-point units (FPUs).

== System Architecture
A modular full-stack architecture ensuring heavy mathematical lifting remains server-side while maintaining edge-ready logic.
- *Backend:* Flask (Python).
- *Frontend:* Single Page Application (SPA) for real-time data visualization.
- *Data Orchestration:* Open-Meteo API for historical training sets.

== Performance Figures
#align(center + horizon)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 5pt,
    image("lodz.png", width: 100%, fit: "contain"),
    image("minsk.png", width: 100%, fit: "contain"),
    image("grodno.png", width: 100%, fit: "contain"),
  )
]

== Challenges: Dealing with Outliers

- *The SLR Weakness:* As seen in the graph, a single "spike" (outlier) can heavily skew a linear trend.
- *The Solution:* This is why we integrate **EWMA**; it provides a recursive "smoothing" effect that is more robust against atmospheric noise than standard regression.

== Portability & Edge Intelligence
- *Portability:* Rely on simple arithmetic, allowing deployment on low-cost hardware.
- *Edge Intelligence:* Local forecasting autonomously without requiring constant internet connectivity once the model is primed.
- *Developing Markets:* High potential for integration in low-cost thermometers for agriculture in developing countries.

== Conclusion & Future Outlook
- *Summary:* A verifiable, low-latency alternative to heavy weather models.
- *Future Work:* Integrating barometric pressure trends to detect non-linear shifts.
- *Impact:* Reducing the cost of localized weather intelligence.

== Links & References
- *Project:* https://github.com/DvorNil/Weather-forecasting/ 
- *Open-Meteo API:* https://open-meteo.com/ 
- *Linear Regression:* Montgomery, D. C. et al. (2021)
- *EWMA Foundation:* Hunter, J. S. (1986).