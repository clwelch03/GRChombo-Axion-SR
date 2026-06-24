/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef INITIALAXIONDATA_HPP_
#define INITIALAXIONDATA_HPP_

#include "Cell.hpp"
#include "Coordinates.hpp"
#include "Potential.hpp"
#include "ScalarField.hpp"
#include "Tensor.hpp"
#include "UserVariables.hpp" //This files needs NUM_VARS - total no. components
#include "VarsTools.hpp"
#include "simd.hpp"

//! Class which sets the initial axion (scalar) cloud on a Kerr BH background.
//! Only the scalar field vars (phi, Pi) are set here; the metric is set
//! separately by the KerrBH class in initialData().
class InitialAxionData
{
  public:
    //! Input params for the initial scalar cloud
    struct params_t
    {
        double amplitude; //!< Peak amplitude of the initial Gaussian cloud
        double width;     //!< Width (sigma) of the Gaussian, in code units
        std::array<double, CH_SPACEDIM>
            center; //!< Centre of the cloud (defaults to grid centre)
    };

    //! The constructor
    InitialAxionData(const params_t a_params, const double a_dx)
        : m_dx(a_dx), m_params(a_params)
    {
    }

    //! Function to compute the value of the initial scalar vars on the grid
    template <class data_t> void compute(Cell<data_t> current_cell) const
    {
        // where am I?
        Coordinates<data_t> coords(current_cell, m_dx, m_params.center);
        data_t r = coords.get_radius();

        // A simple spherical Gaussian cloud, centred on the BH and at rest.
        ScalarField<Potential>::Vars<data_t> scalar_vars;
        scalar_vars.phi =
            m_params.amplitude * exp(-pow(r / m_params.width, 2.0));
        scalar_vars.Pi = 0.0;

        // store only the scalar field vars; the metric is set by KerrBH
        current_cell.store_vars(scalar_vars);
    }

  protected:
    const double m_dx;
    const params_t m_params; //!< The matter initial condition params
};

#endif /* INITIALAXIONDATA_HPP_ */
