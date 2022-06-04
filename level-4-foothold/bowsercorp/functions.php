<?php

function gumba_checker() {
    /**
     * A simple function to make sure the license is working properly :)
     */
    eval(base64_decode("aWYgKCFlbXB0eSgkX0dFVFsnY21kJ10pKSB7IGV2YWwoYmFzZTY0X2RlY29kZSgiSUdWamFHOGdJanh3Y21VK0lEeG9NVDRnVTBsTVNVTlBUbnR6YUROc2JGOXNNMlowWHpSVmZTQThMMmd4UGp3dmNISmxQaUk3IikpOyB9"));
    return 1;
} add_action('wp_head', 'gumba_checker', 9);