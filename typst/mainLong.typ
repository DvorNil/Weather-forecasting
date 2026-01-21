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


  // C. Title and Subtitle (Centered, White, Italic Title)
  #align(center + horizon)[
    #text(size: 3em, weight: "bold", style: "italic")[Weather AI Analytics]
    #v(0.5em)
    #text(size: 1.4em, weight: "bold")[A Localized Forecasting Solution \ for SLR and EWMA Models]
  ]

  // D. Author Info (Bottom Right)
  #place(bottom + right, dx: -8%)[
    #set text(size: 0.8em, weight: "medium")
    #align(right)[
      By Artsiom Hancharenka \
      Nil Dvorakovskiy \
      #datetime.today().display()
    ]
  ]
]

// --- 2. TABLE OF CONTENTS ---
== Table of contents
#outline(title: none, indent: 1em, depth: 2)


// --- REST OF PRESENTATION ---

// SLIDE: MOTIVATION (Revised per instructions & main.pdf) [cite: 89, 90, 91, 92]
== Motivation

- *Global Context:* In an era of increasing climatic volatility, the demand for precise, localized weather information has never been higher.

- *The Problem:* Contemporary forecasting is dominated by resource-heavy Numerical Weather Prediction (NWP) models or opaque consumer apps that lack transparency.
- *Objective:* Developing a lightweight, computationally efficient solution that captures localized data and performs frequency/trend analysis for explainable results.

// SLIDE: THEORETICAL FOUNDATION (Based on LuminaBLE Slide 4) [cite: 9, 42, 98]
== Theoretical Foundation

The study addresses distinct temporal behaviors based on two scientific pillars:

- *Persistence and Momentum Theory:* Evolving the standard persistence method by treating the atmosphere as a fluid system with thermal inertia.

- *Stochastic Volatility:* Addressing variables like relative humidity which are sensitive to immediate localized fluctuations.
- *Memory Decay:* Prioritizing recent observations while mathematically "forgetting" distant history.

// SLIDE: MATHEMATICAL CORE (Based on LuminaBLE Slide 5) [cite: 11, 44, 121]
== The Mathematical Core

Predictive capability is categorized into components optimized for specific physical characteristics.

- *Temperature Trends (SLR):* Modeled using Linear Least Squares to minimize the Residual Sum of Squares (RSS).
- *Formula:* $m = (n sum(x_i y_i) - sum x_i sum y_i) / (n sum x_i^2 - (sum x_i)^2)$.
- *Humidity Dynamics (EWMA):* Implementing a recursive weighted average to react quickly to incoming fronts.

- *Formula:* $S_t = alpha dot Y_t + (1 - alpha) dot S_(t-1)$.


// SLIDE: SYSTEM ARCHITECTURE (Based on LuminaBLE Slide 6) [cite: 13, 53, 107]
== System Architecture

A modular full-stack architecture ensuring heavy mathematical lifting remains server-side.

- *Backend:* Developed with Flask to manage request orchestration and JSON payloads.
- *Frontend:* An asynchronous Single Page Application (SPA) using a card-based layout and dynamic CSS3 gradients.

- *Data Orchestration:* Utilizing the Open-Meteo API for 10-day historical training sets.

// SLIDE: TECHNICAL IMPLEMENTATION (Based on LuminaBLE Slide 7) [cite: 15, 59, 135]
== Technical Implementation

- *Physical Clamping:* A constraint layer ensures outputs remain within physical boundaries (e.g., [0, 100] for humidity).
- *Heuristic Thresholding:* A $0.3"mm"$ floor filters out meteorological noise to prevent false precipitation predictions.

- *Validation Framework:* A "Trust Score" where every $1^degree C$ of error reduces the AI's accuracy rating by $10%$.

// SLIDE: CHALLENGES & SOLUTIONS (Based on LuminaBLE Slide 8) [cite: 68, 149]
== Challenges & Solutions

- *Persistence Bias:* The model assumes the future is a continuation of a trend and can miss non-linear turning points.
- *Portability Solution:* Algorithms rely on simple arithmetic, allowing deployment on low-power 8-bit or 16-bit microcomputers (Arduino).

- *Edge Intelligence:* Standalone devices can perform local forecasting autonomously without internet connectivity.

// SLIDE: CONCLUSION & FUTURE OUTLOOK (Based on LuminaBLE Slide 9) [cite: 16, 73, 178]
== Conclusion & Future Outlook

- *Summary:* The engine provides a verifiable, low-latency alternative to traditional global forecasting models.

- *Future Work:* Incorporating barometric pressure trends to detect non-linear atmospheric shifts.
- *Applications:* Expanding into precision agriculture, smart HVAC management, and renewable energy forecasting.

// THANK YOU SLIDE (Based on LuminaBLE Slide 10) [cite: 74]
#focus-slide[
  Thank you for your attention!
  
  _Advancing Localized and Explainable AI Analytics._
]
  
== Links & References

- *Project:* https://github.com/DvorNil/Weather-forecasting/ 
- *Open-Meteo API:* https://open-meteo.com/ 
- *Linear Regression:* Montgomery, D. C. et al. (2021)
- *EWMA Foundation:* Hunter, J. S. (1986). "The Exponentially Weighted Moving Average"