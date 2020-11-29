(ns plang.components.root
  (:require  [reagent.core :as r]
             [clojure.core.async :refer [go <! >! chan]]
             [cljs-http.client :as http]
             [plang.db :as db]))




;; short cut for reagent-create class
(defn r! [& props]
  (let [params (apply hash-map props)]
    (r/create-class params)))


;; ------ api calls

(def api_url "http://localhost:7001")

(defn api-get! [resource]
  (go
    (let [{:keys [status success body]}
          (<! (http/get (str api_url resource)
                        {:with-credentials? false}))]
      (println "GET" resource status success)
      (if (not (:error body))
        body
        {:error status :body body}))))

(defn api-post! [resource & params]
  (go
    (let [{:keys [status success body]}
          (<! (http/post (str api_url resource)
                         (merge {:with-credentials? false}
                                (apply hash-map params))))]
      (println "POST" resource status success)
      (if success
        body
        {:status status
         :body body
         :error (:error body)}))))

;; ----- business logic ----

(defn get-blocks []
  (let [out* (chan)]
    (-> @db/state :editor .save 
        (.then (fn [x] 
                 (swap! db/state assoc :blocks (js->clj x))
                 (go (>! out* (js->clj x))))))
    out*))


(defn do-check []
  (go 
    (let [blocks (<! (get-blocks))]
     (let [res (<! (api-post! "/check" :json-params blocks))]
       (when (not (:error res))
         (println "r*" res)
         (swap! db/state assoc :out (:out res)))))))

(defn app-root [props]
  (r!
   :component-did-mount
   (fn []
     (swap! db/state assoc :editor (js/EditorJS.)))
   :reagent-render
   (fn [props]
     [:div {:style {:margin "1em"}}
      [:div {:style {:display :flex}}
       [:div.editor_wrapper
        [:div {:id "editorjs"}]]
       [:div.editor_sidebar
        [:div "Wortdefinitionen & Vorschläge"]
        ]]
      [:div.actions
       [:a.btn {:href "#" :on-click do-check} "Check"]]
      (when-not (clojure.string/blank? (@db/state :out))
        [:div.output
         (str (@db/state :out))])])))


