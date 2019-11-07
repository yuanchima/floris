abstract type AbstractWakeModel end

abstract type AbstractTurbine end

struct Jensen <: AbstractWakeModel
    we
end

struct Turbine <: AbstractTurbine
    coord
    rotor_radius
end

struct Coord
    x1
    x2
    x3
end

function loss(x_locations, y_locations, z_locations, turbine::Turbine, 
              deflection_field, flow_field, model::Jensen)
    m = model.we
    x = x_locations - turbine.coord.x1
    b = turbine.rotor_radius

    boundary_line = m * x + b

    y_upper = boundary_line + turbine.coord.x1
end

function mult(x, y, z)
    println(x*y*z)
end

function sum2(x, y)
    println(x + y)
end
