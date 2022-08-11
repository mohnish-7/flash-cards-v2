//////////////////////////////////////////////////////// Delete Deck ////////////////////////////////////////////////////////////////

let edit_deck = new Vue({
  el: '#edit_card',
  delimiters: ['${', '}'],
  data() {
    return {
      card_title: "",
      new_content: "",
      updated: false,
      error: ""
    }
  },
  methods: {
    edit: function() {

      const data = {
        deck_id: d_id,
        card_title: this.card_title,
        new_content: this.new_content
      };
      if (data.card_title.length > 0 && data.new_content.length > 0) {
        fetch('http://127.0.0.1:5000/api/cards', {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
          .then(response => response.json())
          .then(data => {
            console.log(data.length);
            console.log('Success:', data);
            if (data.length > 0) {
              this.error = "";
              this.updated = true;
            } else {
               this.error = data.error_message;
            }

          })
          .catch((error) => {
            console.error('Error:', error);
          });
      } else {
            this.error = "Card name/title or New Content cannot be empty !"
      }


    }
  }
});
