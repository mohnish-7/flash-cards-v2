//////////////////////////////////////////////////////// New Card ////////////////////////////////////////////////////////////////

let new_deck = new Vue({
  el: '#new_card',
  delimiters: ['${', '}'],
  data() {
    return {
      card_title: "",
      card_content: "",
      created: false,
      error: ""
    }
  },
  methods: {
    create: function() {

      const data = {
        username: u_name,
        deck_id: d_id,
        card_title: this.card_title,
        card_content: this.card_content
      };
      if (this.card_title.length > 0 && this.card_content.length > 0) {
        fetch('http://127.0.0.1:5000/api/cards', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
          .then(response => response.json())
          .then(data => {
            console.log('Success:', data);
            if (Object.keys(data).length > 2) {
              this.error = "";
              this.created = true;
            } else {
               this.error = data.error_message;
            }

          })
          .catch((error) => {
            console.error('Error:', error);
          });
      } else {
            this.error = "Card title or Card Content cannot be empty !"
      }


    }
  }
});
