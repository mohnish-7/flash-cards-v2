//////////////////////////////////////////////////////// New Deck ////////////////////////////////////////////////////////////////

let new_deck = new Vue({
  el: '#new_deck',
  delimiters: ['${', '}'],
  data() {
    return {
      deck_name: "",
      created: false,
      error: ""
    }
  },
  methods: {
    create: function() {

      const data = {
        username: u_name,
        deck_name: this.deck_name
      };
      if (data.username.length > 0 && data.deck_name.length > 0) {
        fetch('http://127.0.0.1:5000/api/decks', {
            method: 'POST', // or 'PUT'
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
            this.error = error.error_msg;
          });
      } else {
            this.error = "Deck Name cannot be empty !"
      }


    }
  }
});
