(defproject plang "0.1.0"
  :dependencies [[org.clojure/clojure "1.10.1"]
                 [thheller/shadow-cljs "2.10.18"]
                 [org.clojure/core.async "1.3.610"]
                 [reagent "1.0.0-alpha2"]
                 [cljs-http "0.1.46"]]

  :plugins [[lein-ancient "0.6.15"]
            [lein-less "1.7.5"]]

  :less {:source-paths ["src/less"]
         :target-path   "public/css"}

  :min-lein-version "2.8.3"

  :source-paths ["src"]

  :clean-targets ^{:protect false} ["public/js/compiled"]

  :aliases {"dev"  ["with-profile" "dev" "run" "-m" "shadow.cljs.devtools.cli" "watch" "app"]
            "prod" ["with-profile" "prod" "run" "-m" "shadow.cljs.devtools.cli" "release" "app"]}

  :profiles
  {:dev
   {:dependencies [[binaryage/devtools "1.0.2"]]
    :preloads [devtools.preloads]}})
