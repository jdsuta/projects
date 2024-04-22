// Pending archvie unarchive button.
// Need to add eventlistener for onclick and take actions appropriately.

document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(sender, subject, body, timestamp) {


  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#show-email').style.display = 'none';

  if (sender === undefined || subject === undefined || body === undefined || timestamp === undefined ) {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
  else {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = sender;

    // Adding RE to subject
    // Using regex to check match for RE: if there's a RE we will not append it
    // https://www.w3schools.com/js/js_regexp.asp
    let text = subject;
    let n = text.search("Re:");
    if (n === 0) {
      document.querySelector('#compose-subject').value = `${subject}`;
    }
    else {
      document.querySelector('#compose-subject').value = `Re: ${subject}`;
    }

    // I was doing it wrong since the timestamp is already passed to us via API. However, this might work in future 
    // To add date when replying. https://www.w3schools.com/js/js_dates.asp, https://www.w3schools.com/js/js_date_methods.asp 
    // // Example: "On Jan 1 2020, 12:00 AM foo@example.com wrote:"
    // const d = new Date();

    // // Month is returned as a number so we need to conver it to actual month using array
    // const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    // let hours = d.getHours()

    // let meridian = ""
    // // Since hours are in format 0-23 we need to convert it to 12 format and add AM or PM. For this case the remainder is used
    // if (hours > 12){
    //   hours = hours % 12
    //   meridian = "PM"
    // }
    // else {
    //   meridian = "AM"
    // }

    // Added \n\n to add spaces and organizze the emails better.
    // datereply = `On ${months[d.getMonth()]} ${d.getDate()} ${d.getFullYear()}, ${hours}:${d.getMinutes()} ${meridian} ${sender} wrote: \n\n`

    datereply = `On ${timestamp} ${sender} wrote: \n\n`

    document.querySelector('#compose-body').value = '\n\n' + '---' + '\n\n' + datereply + body;
  }


  //Sends email
  document.querySelector('form').onsubmit = function () {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    console.log(body);

    // API to send email
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
        // load the user’s sent mailbo and wait until is sent    
      load_mailbox('sent');
    });
    
    // Stop form from submitting. SUPER IMPORTANT. Otherwise it will reload the page and will process it again...
    return false;
  }
}


var tbody = document.createElement("tbody");

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#emails').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#show-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      // to initialize the inner HTML and don't acumulate emails over and over again
      document.querySelector('#emails').innerHTML = '';

      // Print emails
      console.log(emails);
      // console.log(emails.length);

      // Check if mailbox is equal to sent:

      const table = document.createElement("table");

      //Initialize tables tbody so they are clean and do not store previous data. 
      table.innerHTML = '';
      tbody.innerHTML = '';

      table.classList.add("table", "table-hover", "table-sm");

      // var tbody =  document.createElement("tbody");

      if (mailbox === 'sent') {
        const headers = `
        <thead>
          <tr>
            <th>To</th>
            <th>Subject</th>
            <th>timestamp</th>
          </tr>
        </thead>`

        // Only is possible to use once innerHTML if you use it 2+ times it will overwrite latest change
        // However, it you use it once and then use append method it will construct it accordingly. 
        table.innerHTML = headers;

        getemails(emails, mailbox)
        table.append(tbody)
        // the append method expects DOM nodes or DOMString objects as arguments, not HTML strings.
        document.querySelector('#emails').append(table);
      }

      else if (mailbox === 'inbox') {
        const headers = `
        <thead>
          <tr>
            <th>From</th>
            <th>Subject</th>
            <th>timestamp</th>
          </tr>
        </thead>`

        table.innerHTML = headers;

        getemails(emails, mailbox)
        table.append(tbody)
        // the append method expects DOM nodes or DOMString objects as arguments, not HTML strings.
        document.querySelector('#emails').append(table);
      }

      else if (mailbox === 'archive') {
        const headers = `
        <thead>
          <tr>
            <th>From</th>
            <th>To</th>
            <th>Subject</th>
            <th>timestamp</th>
          </tr>
        </thead>`

        table.innerHTML = headers;

        getemails(emails, mailbox)
        table.append(tbody)
        // the append method expects DOM nodes or DOMString objects as arguments, not HTML strings.
        document.querySelector('#emails').append(table);
      }
    });
}

function accessemail(id, mailbox) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // Print email
      // console.log(email);
      // from email we recover all the neccesary data and then store it accordingly.

      const sender = email.sender;
      const recipients = email.recipients;
      const subject = email.subject;
      const timestamp = email.timestamp;
      let body = email.body;

      // Show the mailbox and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#emails').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#show-email').style.display = 'block';

      // Show the mail under div #show-email
      // Created another id email-archive to insert button to archive or unarchvie email
      
      // The body was modified so it it's rendered human firendly and readable. 
      // The /g in /---/g is a flag in JavaScript regular expressions that stands for "global". This was taken from CS50 AI rubber duck
      body = body.replace(/---/g, "<hr>");
      body = body.replace(/\n\n/g, "<br><br>");

      document.querySelector('#show-email').innerHTML = `
          <div class="card-header">
            <strong>From:</strong>${sender}
              <br>
              <strong>To:</strong> ${recipients}
              <br>
              <strong>Subject:</strong> ${subject}
              <br>
              <strong>Timestamp:</strong> ${timestamp}
          </div>
          <div class="card-body">
            <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
            <br>
            <br>
            <p class="card-text">           
            ${body}</p>
            <div class="text-right" id="email-archive"></div>
          </div>
          `;

      // once has accessed the email it will mark it as email read 
      // This only applies to inbox email
      if (mailbox === 'inbox') {
        reademail(id)
      }
      if (mailbox === 'inbox' || mailbox === 'archive') {
        arUNchive(id, mailbox)
      }

      //Checking when the user clicks reply to load compose email and reply
      document.querySelector('#reply').addEventListener('click', () => compose_email(sender, subject, body, timestamp));

    });
}






//Archive UnArchive button
function arUNchive(id, mailbox) {
  let button = document.createElement("button")
  // Insert button in the previously created HTML. Inside card-body
  document.querySelector('#email-archive').append(button)
  button.setAttribute("type", "button")
  button.setAttribute("class", "btn btn-primary btn-sm")

  if (mailbox === "archive") {
    button.innerHTML = "Unarchive"
    // Only Archive when the button is clicked
    button.onclick = () => {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: false
        })
      })
      // Introduce a little delay because it was executing so fast the load mailbox function that it was loading old data
      setTimeout(function () {
        load_mailbox('inbox')
      }, 50);
    }
  }
  else {
    button.innerHTML = "Archive"
    // Only unarchive when the button is clicked
    button.onclick = () => {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: true
        })
      })
      // Introduce a little delay because it was executing so fast the load mailbox function that it was loading old data
      setTimeout(function () {
        load_mailbox('inbox')
      }, 50);
    }
  }
}


function reademail(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

function getemails(emails, mailbox) {

  for (let i = 0; i < emails.length; i++) {

    let sender = emails[i].sender;
    let recipients = emails[i].recipients;
    let subject = emails[i].subject;
    let timestamp = emails[i].timestamp;
    let id = emails[i].id;
    let read = emails[i].read;

    const tr = document.createElement("tr");

    // assigns an onclick event to the tr element. 
    tr.onclick = function () { accessemail(id, mailbox) };


    let mail = '';

    if (mailbox === 'sent') {
      mail = `
      <td>${recipients}</td>
      <td>${subject}</td>
      <td>${timestamp}</td>`;
    }

    if (mailbox === 'inbox') {

      if (read === true) {
        console.log(`This email ${id} has been read`)
        tr.style.backgroundColor = "#E6E6E6";
        //tr.setAttribute("class", "bg-light")
      }

      mail = `
      <td>${sender}</td>
      <td>${subject}</td>
      <td>${timestamp}</td>`;
    }

    if (mailbox === 'archive') {
      mail = `
      <td>${sender}</td>
      <td>${recipients}</td>
      <td>${subject}</td>
      <td>${timestamp}</td>`;
    }


    tr.innerHTML = mail
    tbody.append(tr);
  }
}
