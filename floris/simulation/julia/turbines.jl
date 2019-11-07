abstract type AbstractTurbine end

struct Turbine <: AbstractTurbine
    coord
    rotor_diameter
    hub_height
    aI
end

struct Coord
    x1
    x2
    x3
end
