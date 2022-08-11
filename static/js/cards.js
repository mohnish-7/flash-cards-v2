//////////////////////////////////////////////////////// Cards ////////////////////////////////////////////////////////////////

Vue.component('flash-card', {
  props: ['card_title', 'card_id', 'card_content'],
  data: function () {
    return {
      hreference: "#answer",
      c_id: ""
    }
  },
  template: `
  <div>
      <p class="question">{{card_title}}</p>
      <a id="answer-btn" class="btn btn-primary q-btn ans-btn" data-bs-toggle="collapse" :href="hreference" role="button" aria-expanded="false" >
        Answer
      </a>
    <div>
      <div class="collapse answer" id="answer">
        <div class="card card-body explanation">
          {{card_content}}
        </div>
      </div>
    </div>
  </div>
  `
})

let dashboard = new Vue({
  el: '#cards',
  delimiters: ['${', '}'],
  data() {
    return {
      title: "Flash Cards"
    }
  }
});
