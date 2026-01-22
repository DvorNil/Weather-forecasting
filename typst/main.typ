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
    #text(size: 1.4em, weight: "bold")[A Localized Weather Forecasting Solution]
  ]

  // D. Author Info (Bottom Right)
  #place(bottom + right, dx: -8%)[
    #set text(size: 0.8em, weight: "medium")
    #align(right)[
      By Artsiom Hancharenka \
      Nil Dvorakovskiy \
      FAMCS BSU, group 3 
    ]
  ]
  #place(bottom + center)[
    #align(center)[
      Minsk 2026
    ]
  ]
]

// --- 2. TABLE OF CONTENTS ---
== Table of contents
#outline(title: none, indent: 1em, depth: 2)


// --- REST OF PRESENTATION ---

// SLIDE: MOTIVATION (Revised per instructions & main.pdf) [cite: 89, 90, 91, 92]
== Motivation

- *Global Context:* Demand for precise, localized weather information.

- *The Problem:* Domination of resource-heavy models.
- *Objective:* Lightweight, computationally efficient solution.

// SLIDE: THEORETICAL FOUNDATION (Based on LuminaBLE Slide 4) [cite: 9, 42, 98]
== Theoretical Foundation


#text(size: 30pt)[Two scientific pillars:]

#linebreak(justify: true)

- *Persistence and Momentum Theory:* Atmosphere as a fluid system.

- *Chaotic Volatility:* Sensitive to immediate localized fluctuations.

== Objective
#grid(
  columns: (1fr, 1.2fr), // Text takes 1 part, Image takes 1.2 parts
  gutter: 20pt,
  align: horizon,       
  [
    #set text(size: 1.5em) 
    - *The goal:* Prove the correctness of algorithm.
  ],
  figure(
    image("proof.jpeg", width: 100%),
  )
)

// instead of slide with math core, remove forumulas,  change topic for aim : develop website to check and prove the Theory
// add practical usage

// SLIDE: SYSTEM ARCHITECTURE (Based on LuminaBLE Slide 6) [cite: 13, 53, 107]
== System Architecture

- *Backend:* Flask.
- *Frontend:* SPA with dynamic elements.
- *Data Orchestration:* Open-Meteo API for historical training sets.

== Figures
 #figure( image("lodz.png", width: 80%))

== Challenges: Dealing with Outliers
#figure( image("regression.png", width: 80%))


// SLIDE: CHALLENGES & SOLUTIONS (Based on LuminaBLE Slide 8) [cite: 68, 149]
#grid(
  columns: (1.5fr, 1fr), // Text gets more space than the image
  gutter: 15pt,          // Space between text and image
  align: horizon,        // Vertically centers both elements
  [
    - *Portability Solution:* Deployment on low-power 8-bit microcomputers.
    #v(1em) // Adds spacing between the bullets
    - *Edge Intelligence:* Local forecasting without Internet.
  ],
  figure(
    image("thermometer.png", width: 100%),
  )
)

// SLIDE: CONCLUSION & FUTURE OUTLOOK (Based on LuminaBLE Slide 9) [cite: 16, 73, 178]
== Conclusion & Future Outlook

- *Summary:* Verifiable, low-latency alternative.

- *Future Work:* Thermometer prototypes.

- *Applications:*  Technology utilizing in developing countries. 

  
== Links & References

- *Project:* https://github.com/DvorNil/Weather-forecasting/ 
- *Open-Meteo API:* https://open-meteo.com/ 
- *Linear Regression:* Montgomery, D. C. et al. (2021)
- *EWMA Foundation:* Hunter, J. S. (1986). "The Exponentially Weighted Moving Average"
