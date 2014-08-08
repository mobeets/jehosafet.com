function create_axes() {
    yds = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110];
    axis_vals = yds.join('<br>');
    $('.x-axis').html(axis_vals);
    $('.y-axis').html(axis_vals);

    fs = [512, 256, 128, 64, 32, 16, 8, 4, 2, 1];
    axis_vals = fs.join('<br>');
    $('.legend-axis').html(axis_vals);
}
function toggle_visible() {
    val = this.value;
    $('#' + val).toggle(this.checked);
}
$(function() {
    $('img.im-overlay').css('display', 'none');
    create_axes();
    $('.toggle').click(toggle_visible);
});
