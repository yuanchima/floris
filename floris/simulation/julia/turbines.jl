abstract type AbstractTurbine end

struct Turbine <: AbstractTurbine
    coord
    rotor_radius
    hub_height
end

struct Coord
    x1
    x2
    x3
end
