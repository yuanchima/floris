include("wake_velocity.jl")

params = Jensen(0.3)

coord = Coord([0.,500.],[0.,100.],[90.,90.])
turbine = Turbine(coord,100.,90.,2.0/3.0)

xlocs = ones(50)*coord.x1[2]
ylocs = collect(-49:2:49)
zlocs = ones(50)*coord.x3[2]
deflection_field = [0.,0.]

struct FF
    u_initial
end

flow_field = FF([10.,10.])
println(turbine.coord.x1)

loss_val = loss(xlocs[1], ylocs[1], zlocs[1], turbine,
              deflection_field, flow_field, params)

println(loss_val)
