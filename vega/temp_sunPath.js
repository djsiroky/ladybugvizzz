hours = []
pos = []
posObj = []

Date.prototype.addMonth = function(m){
    this.setMonth(this.getMonth()+m);
    return this;
}

Date.prototype.addHours = function(h){
    this.setHours(this.getHours()+h);
    return this;
}
//Loop
hours.push(new Date().addMonth(-1).addHours(-10))

hours.forEach(hour => { pos.push(solarCalculator([39.0839389, -94.5818676]).position(hour)) })

pos.forEach(item => { posObj.push({"size": 100, "lon": item[0], "lat": item[1]}) })




var coords3 = d3.utcDays(start, end).map(function(day) {
    return hours.map(hour => { return {"hour": hour, "month": (1 + day.getMonth()), "date": day.getDate(), "pos": solar.position(d3.utcHour.offset(day, hour))} })
})
flat = [].concat.apply([], coords3)