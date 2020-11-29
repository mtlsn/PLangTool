(ns plang.index
  (:require [reagent.dom :as rd]
            [plang.components.root :refer [app-root]]))


(enable-console-print!)

(defn main! []
  (.log js/console "Plang App v0.1\nPavel Metelitsyn 2020\npavel@metelitsyn.de")
  (rd/render [app-root] (.getElementById js/document "app")))
