num = Math.floor(Math.random() * 5);
switch (num) {

    case 1: //funguje
        document.body.style.backgroundImage = "url('https://media.discordapp.net/attachments/788128967056031755/844526700720685086/unknown.png?width=530&height=406')"

        break;
    case 2: //funguje
        document.body.style.backgroundImage = "url('https://media.discordapp.net/attachments/788128967056031755/844526658652602398/unknown.png')"
        break;


    case 3: //funguje
        document.body.style.color = "black";
        document.body.style.backgroundImage = "url('https://media.discordapp.net/attachments/788128967056031755/844519906748792872/unknown.png?width=537&height=406')"

        break;
    case 4: //funguje
        document.body.style.color = "black";
        document.body.style.backgroundImage = "url('https://media.discordapp.net/attachments/788128967056031755/844525627256078336/unknown.png?width=444&height=406')"
        break;
    default:
        document.body.style.color = "black";
        console.log("Default")
        break;

}