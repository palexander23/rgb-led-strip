class LEDStrip {

    constructor(ip = "192.168.0.107") {
        this.addr = "http://" + ip
        this.xhttp = new XMLHttpRequest();
    }

    switch(red, gre, blu) {

        var red_str
        var gre_str
        var blu_str

        if (red) {
            red_str = "ON"
        }
        else {
            red_str = "OFF"
        }

        if (gre) {
            gre_str = "ON"
        }
        else {
            gre_str = "OFF"
        }

        if (blu) {
            blu_str = "ON"
        }
        else {
            blu_str = "OFF"
        }

        var body_obj = { mode: "switch", red: red_str, blu: blu_str, gre: gre_str }
        var body_str = JSON.stringify(body_obj)

        this.post_req(body_str)
    }

    analog(colour) {
        var body_obj = { mode: "analog", colour: colour }
        var body_str = JSON.stringify(body_obj)

        this.post_req(body_str)
    }

    flash(colour_list, on_time_list) {
        var body_obj = { mode: "flash", colour_list: colour_list, on_time_list: on_time_list }
        var body_str = JSON.stringify(body_obj)

        this.post_req(body_str)
    }

    fade(colour_list, on_time_list, fade_time_list) {
        var body_obj = { mode: "fade", colour_list: colour_list, on_time_list: on_time_list, fade_time_list: fade_time_list }
        var body_str = JSON.stringify(body_obj)

        this.post_req(body_str)
    }

    post_req(body_str) {
        this.xhttp.open("POST", this.addr, true)
        this.xhttp.send(body_str)
        console.log("Request completed")
    }

}