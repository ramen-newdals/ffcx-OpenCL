"Code snippets for code generation"

__author__ = "Anders Logg (logg@simula.no)"
__date__ = "2007-02-28 -- 2007-04-18"
__copyright__ = "Copyright (C) 2007 Anders Logg"
__license__  = "GNU GPL version 3 or any later version"

# Modified by Kristian Oelgaard 2007
# Modified by Marie Rognes 2007, 2008

# Code snippet for computing the Jacobian, its inverse and determinant in 1D
jacobian_1D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
  
// Compute determinant of Jacobian
double detJ%(restriction)s = J%(restriction)s_00;
  
// Compute inverse of Jacobian
const double Jinv%(restriction)s_00 =  1.0 / detJ%(restriction)s;"""

# Code snippet for computing the Jacobian, its inverse and determinant in 2D
jacobian_2D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];
  
// Compute determinant of Jacobian
double detJ%(restriction)s = J%(restriction)s_00*J%(restriction)s_11 - J%(restriction)s_01*J%(restriction)s_10;
  
// Compute inverse of Jacobian
const double Jinv%(restriction)s_00 =  J%(restriction)s_11 / detJ%(restriction)s;
const double Jinv%(restriction)s_01 = -J%(restriction)s_01 / detJ%(restriction)s;
const double Jinv%(restriction)s_10 = -J%(restriction)s_10 / detJ%(restriction)s;
const double Jinv%(restriction)s_11 =  J%(restriction)s_00 / detJ%(restriction)s;"""

# Code snippet for computing the Jacobian, its inverse and determinant in 3D
jacobian_3D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_02 = x%(restriction)s[3][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];
const double J%(restriction)s_12 = x%(restriction)s[3][1] - x%(restriction)s[0][1];
const double J%(restriction)s_20 = x%(restriction)s[1][2] - x%(restriction)s[0][2];
const double J%(restriction)s_21 = x%(restriction)s[2][2] - x%(restriction)s[0][2];
const double J%(restriction)s_22 = x%(restriction)s[3][2] - x%(restriction)s[0][2];
  
// Compute sub determinants
const double d%(restriction)s_00 = J%(restriction)s_11*J%(restriction)s_22 - J%(restriction)s_12*J%(restriction)s_21;
const double d%(restriction)s_01 = J%(restriction)s_12*J%(restriction)s_20 - J%(restriction)s_10*J%(restriction)s_22;
const double d%(restriction)s_02 = J%(restriction)s_10*J%(restriction)s_21 - J%(restriction)s_11*J%(restriction)s_20;

const double d%(restriction)s_10 = J%(restriction)s_02*J%(restriction)s_21 - J%(restriction)s_01*J%(restriction)s_22;
const double d%(restriction)s_11 = J%(restriction)s_00*J%(restriction)s_22 - J%(restriction)s_02*J%(restriction)s_20;
const double d%(restriction)s_12 = J%(restriction)s_01*J%(restriction)s_20 - J%(restriction)s_00*J%(restriction)s_21;

const double d%(restriction)s_20 = J%(restriction)s_01*J%(restriction)s_12 - J%(restriction)s_02*J%(restriction)s_11;
const double d%(restriction)s_21 = J%(restriction)s_02*J%(restriction)s_10 - J%(restriction)s_00*J%(restriction)s_12;
const double d%(restriction)s_22 = J%(restriction)s_00*J%(restriction)s_11 - J%(restriction)s_01*J%(restriction)s_10;
  
// Compute determinant of Jacobian
double detJ%(restriction)s = J%(restriction)s_00*d%(restriction)s_00 + J%(restriction)s_10*d%(restriction)s_10 + J%(restriction)s_20*d%(restriction)s_20;
  
// Compute inverse of Jacobian
const double Jinv%(restriction)s_00 = d%(restriction)s_00 / detJ%(restriction)s;
const double Jinv%(restriction)s_01 = d%(restriction)s_10 / detJ%(restriction)s;
const double Jinv%(restriction)s_02 = d%(restriction)s_20 / detJ%(restriction)s;
const double Jinv%(restriction)s_10 = d%(restriction)s_01 / detJ%(restriction)s;
const double Jinv%(restriction)s_11 = d%(restriction)s_11 / detJ%(restriction)s;
const double Jinv%(restriction)s_12 = d%(restriction)s_21 / detJ%(restriction)s;
const double Jinv%(restriction)s_20 = d%(restriction)s_02 / detJ%(restriction)s;
const double Jinv%(restriction)s_21 = d%(restriction)s_12 / detJ%(restriction)s;
const double Jinv%(restriction)s_22 = d%(restriction)s_22 / detJ%(restriction)s;"""

# Code snippet for computing the scale factor (determinant)
scale_factor = """\
// Set scale factor
const double det = std::abs(detJ);
"""

# Code snippet for computing the determinant of the facet mapping in 1D
facet_determinant_1D = """\
// Facet determinant 1D (vertex)
const double det = 1.0;
"""

# Code snippet for computing the determinant of the facet mapping in 2D
facet_determinant_2D = """\
// Vertices on edges
static unsigned int edge_vertices[3][2] = {{1, 2}, {0, 2}, {0, 1}};

// Get vertices
const unsigned int v0 = edge_vertices[%(facet)s][0];
const unsigned int v1 = edge_vertices[%(facet)s][1];

// Compute scale factor (length of edge scaled by length of reference interval)
const double dx0 = x%(restriction)s[v1][0] - x%(restriction)s[v0][0];
const double dx1 = x%(restriction)s[v1][1] - x%(restriction)s[v0][1];
const double det = std::sqrt(dx0*dx0 + dx1*dx1);
"""

# Code snippet for computing the determinant of the facet mapping in 3D
facet_determinant_3D = """\
// Vertices on faces
static unsigned int face_vertices[4][3] = {{1, 2, 3}, {0, 2, 3}, {0, 1, 3}, {0, 1, 2}};

// Get vertices
const unsigned int v0 = face_vertices[%(facet)s][0];
const unsigned int v1 = face_vertices[%(facet)s][1];
const unsigned int v2 = face_vertices[%(facet)s][2];

// Compute scale factor (area of face scaled by area of reference triangle)
const double a0 = (x%(restriction)s[v0][1]*x%(restriction)s[v1][2] + x%(restriction)s[v0][2]*x%(restriction)s[v2][1] + x%(restriction)s[v1][1]*x%(restriction)s[v2][2])
              - (x%(restriction)s[v2][1]*x%(restriction)s[v1][2] + x%(restriction)s[v2][2]*x%(restriction)s[v0][1] + x%(restriction)s[v1][1]*x%(restriction)s[v0][2]);
const double a1 = (x%(restriction)s[v0][2]*x%(restriction)s[v1][0] + x%(restriction)s[v0][0]*x%(restriction)s[v2][2] + x%(restriction)s[v1][2]*x%(restriction)s[v2][0])
              - (x%(restriction)s[v2][2]*x%(restriction)s[v1][0] + x%(restriction)s[v2][0]*x%(restriction)s[v0][2] + x%(restriction)s[v1][2]*x%(restriction)s[v0][0]);
const double a2 = (x%(restriction)s[v0][0]*x%(restriction)s[v1][1] + x%(restriction)s[v0][1]*x%(restriction)s[v2][0] + x%(restriction)s[v1][0]*x%(restriction)s[v2][1])
              - (x%(restriction)s[v2][0]*x%(restriction)s[v1][1] + x%(restriction)s[v2][1]*x%(restriction)s[v0][0] + x%(restriction)s[v1][0]*x%(restriction)s[v0][1]);
const double det = std::sqrt(a0*a0 + a1*a1 + a2*a2);
"""

# Code snippet for evaluate_dof in 1D
evaluate_dof_1D = """\
double values[%d];
double coordinates[1];

// Nodal coordinates on reference cell
static double X[%d][1] = %s;

// Components for each dof
static unsigned int components[%d] = %s;

// Extract vertex coordinates
const double * const * x = c.coordinates;

// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X[i][0];
const double w1 = X[i][0];

// Compute affine mapping x = F(X)
coordinates[0] = w0*x[0][0] + w1*x[1][0];

// Evaluate function at coordinates
f.evaluate(values, coordinates, c);

// Pick component for evaluation
return values[components[i]];"""

# Code snippet for evaluate_dof in 2D
evaluate_dof_2D = """\
double values[%d];
double coordinates[2];

// Nodal coordinates on reference cell
static double X[%d][2] = %s;

// Components for each dof
static unsigned int components[%d] = %s;

// Extract vertex coordinates
const double * const * x = c.coordinates;

// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X[i][0] - X[i][1];
const double w1 = X[i][0];
const double w2 = X[i][1];

// Compute affine mapping x = F(X)
coordinates[0] = w0*x[0][0] + w1*x[1][0] + w2*x[2][0];
coordinates[1] = w0*x[0][1] + w1*x[1][1] + w2*x[2][1];

// Evaluate function at coordinates
f.evaluate(values, coordinates, c);

// Pick component for evaluation
return values[components[i]];"""

# Code snippet for evaluate_dof in 3D
evaluate_dof_3D = """\
double values[%d];
double coordinates[3];

// Nodal coordinates on reference cell
static double X[%d][3] = %s;

// Components for each dof
static unsigned int components[%d] = %s;

// Extract vertex coordinates
const double * const * x = c.coordinates;

// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X[i][0] - X[i][1] - X[i][2];
const double w1 = X[i][0];
const double w2 = X[i][1];
const double w3 = X[i][2];

// Compute affine mapping x = F(X)
coordinates[0] = w0*x[0][0] + w1*x[1][0] + w2*x[2][0] + w3*x[3][0];
coordinates[1] = w0*x[0][1] + w1*x[1][1] + w2*x[2][1] + w3*x[3][1];
coordinates[2] = w0*x[0][2] + w1*x[1][2] + w2*x[2][2] + w3*x[3][2];

// Evaluate function at coordinates
f.evaluate(values, coordinates, c);

// Pick component for evaluation
return values[components[i]];"""

# Code snippet for eta basis on intervals (reproduced from FIAT reference.py)
eta_interval_snippet = """\
x = 2.0*x - 1.0;
"""

# Code snippet for eta basis on triangles (reproduced from FIAT reference.py)
eta_triangle_snippet = """\
if (std::abs(y - 1.0) < %s)
  x = -1.0;
else
  x = 2.0 *x/(1.0 - y) - 1.0;
y = 2.0*y - 1.0;"""

# Code snippet for eta basis on tetrahedra (reproduced from FIAT reference.py)
eta_tetrahedron_snippet = """\
if (std::abs(y + z - 1.0) < %s)
  x = 1.0;
else
  x = -2.0 * x/(y + z - 1.0) - 1.0;
if (std::abs(z - 1.0) < %s)
  y = -1.0;
else
  y = 2.0 * y/(1.0 - z) - 1.0;
z = 2.0 * z - 1.0;"""

# Map basis function to local basisfunction, used by 'evaluate_basis.py'
evaluate_basis_dof_map = """\
unsigned int element = 0;
unsigned int tmp = 0;
for (unsigned int j = 0; j < %d; j++)
{
  if (tmp +  dofs_per_element[j] > i)
  {
    i -= tmp;
    element = element_types[j];
    break;
  }
  else
    tmp += dofs_per_element[j];


}"""

# Inverse affine map from physical cell to UFC reference cell in 1D
map_coordinates_1D = """\
// Extract vertex coordinates
const double * const * element_coordinates = c.coordinates;

// Compute Jacobian of affine map from reference cell
const double J_00 = element_coordinates[1][0] - element_coordinates[0][0];

// Get coordinates and map to the reference (UFC) element
double x = (coordinates[0] - element_coordinates[0][0]) / J_00;"""

# Inverse affine map from physical cell to UFC reference cell in 2D
map_coordinates_2D = """\
// Extract vertex coordinates
const double * const * element_coordinates = c.coordinates;

// Compute Jacobian of affine map from reference cell
const double J_00 = element_coordinates[1][0] - element_coordinates[0][0];
const double J_01 = element_coordinates[2][0] - element_coordinates[0][0];
const double J_10 = element_coordinates[1][1] - element_coordinates[0][1];
const double J_11 = element_coordinates[2][1] - element_coordinates[0][1];
  
// Compute determinant of Jacobian
const double detJ = J_00*J_11 - J_01*J_10;

// Compute inverse of Jacobian
const double Jinv_00 =  J_11 / detJ;
const double Jinv_01 = -J_01 / detJ;
const double Jinv_10 = -J_10 / detJ;
const double Jinv_11 =  J_00 / detJ;

// Get coordinates and map to the reference (UFC) element
double x = (element_coordinates[0][1]*element_coordinates[2][0] -\\
            element_coordinates[0][0]*element_coordinates[2][1] +\\
            J_11*coordinates[0] - J_01*coordinates[1]) / detJ;
double y = (element_coordinates[1][1]*element_coordinates[0][0] -\\
            element_coordinates[1][0]*element_coordinates[0][1] -\\
            J_10*coordinates[0] + J_00*coordinates[1]) / detJ;"""

# Inverse affine map from physical cell to the UFC reference cell in 3D
map_coordinates_3D = """\
// Extract vertex coordinates
const double * const * element_coordinates = c.coordinates;

// Compute Jacobian of affine map from reference cell
const double J_00 = element_coordinates[1][0] - element_coordinates[0][0];
const double J_01 = element_coordinates[2][0] - element_coordinates[0][0];
const double J_02 = element_coordinates[3][0] - element_coordinates[0][0];
const double J_10 = element_coordinates[1][1] - element_coordinates[0][1];
const double J_11 = element_coordinates[2][1] - element_coordinates[0][1];
const double J_12 = element_coordinates[3][1] - element_coordinates[0][1];
const double J_20 = element_coordinates[1][2] - element_coordinates[0][2];
const double J_21 = element_coordinates[2][2] - element_coordinates[0][2];
const double J_22 = element_coordinates[3][2] - element_coordinates[0][2];
  
// Compute sub determinants
const double d00 = J_11*J_22 - J_12*J_21;
const double d01 = J_12*J_20 - J_10*J_22;
const double d02 = J_10*J_21 - J_11*J_20;

const double d10 = J_02*J_21 - J_01*J_22;
const double d11 = J_00*J_22 - J_02*J_20;
const double d12 = J_01*J_20 - J_00*J_21;

const double d20 = J_01*J_12 - J_02*J_11;
const double d21 = J_02*J_10 - J_00*J_12;
const double d22 = J_00*J_11 - J_01*J_10;
  
// Compute determinant of Jacobian
double detJ = J_00*d00 + J_10*d10 + J_20*d20;

// Compute inverse of Jacobian
const double Jinv_00 = d00 / detJ;
const double Jinv_01 = d10 / detJ;
const double Jinv_02 = d20 / detJ;
const double Jinv_10 = d01 / detJ;
const double Jinv_11 = d11 / detJ;
const double Jinv_12 = d21 / detJ;
const double Jinv_20 = d02 / detJ;
const double Jinv_21 = d12 / detJ;
const double Jinv_22 = d22 / detJ;

// Compute constants
const double C0 = d00*(element_coordinates[0][0] - element_coordinates[2][0] - element_coordinates[3][0]) \\
                + d10*(element_coordinates[0][1] - element_coordinates[2][1] - element_coordinates[3][1]) \\
                + d20*(element_coordinates[0][2] - element_coordinates[2][2] - element_coordinates[3][2]);

const double C1 = d01*(element_coordinates[0][0] - element_coordinates[1][0] - element_coordinates[3][0]) \\
                + d11*(element_coordinates[0][1] - element_coordinates[1][1] - element_coordinates[3][1]) \\
                + d21*(element_coordinates[0][2] - element_coordinates[1][2] - element_coordinates[3][2]);

const double C2 = d02*(element_coordinates[0][0] - element_coordinates[1][0] - element_coordinates[2][0]) \\
                + d12*(element_coordinates[0][1] - element_coordinates[1][1] - element_coordinates[2][1]) \\
                + d22*(element_coordinates[0][2] - element_coordinates[1][2] - element_coordinates[2][2]);

// Get coordinates and map to the UFC reference element
double x = (C0 + d00*coordinates[0] + d10*coordinates[1] + d20*coordinates[2]) / detJ;
double y = (C1 + d01*coordinates[0] + d11*coordinates[1] + d21*coordinates[2]) / detJ;
double z = (C2 + d02*coordinates[0] + d12*coordinates[1] + d22*coordinates[2]) / detJ;"""


# Inverse affine map from physical cell to the FIAT reference cell in 2D
map_coordinates_FIAT_2D = """\
// Extract vertex coordinates
const double * const * element_coordinates = c.coordinates;

// Compute Jacobian of affine map from reference cell
const double J_00 = element_coordinates[1][0] - element_coordinates[0][0];
const double J_01 = element_coordinates[2][0] - element_coordinates[0][0];
const double J_10 = element_coordinates[1][1] - element_coordinates[0][1];
const double J_11 = element_coordinates[2][1] - element_coordinates[0][1];
  
// Compute determinant of Jacobian
const double detJ = J_00*J_11 - J_01*J_10;

// Compute constants
const double C0 = element_coordinates[1][0] + element_coordinates[2][0];
const double C1 = element_coordinates[1][1] + element_coordinates[2][1];

// Get coordinates and map to the reference (FIAT) element
double x = (J_01*C1 - J_11*C0 + 2.0*J_11*coordinates[0] - 2.0*J_01*coordinates[1]) / detJ;
double y = (J_10*C0 - J_00*C1 - 2.0*J_10*coordinates[0] + 2.0*J_00*coordinates[1]) / detJ;"""

# Inverse affine map from physical cell to (FIAT) reference cell in 3D
map_coordinates_FIAT_3D = """\
// Extract vertex coordinates
const double * const * element_coordinates = c.coordinates;

// Compute Jacobian of affine map from reference cell
const double J_00 = element_coordinates[1][0] - element_coordinates[0][0];
const double J_01 = element_coordinates[2][0] - element_coordinates[0][0];
const double J_02 = element_coordinates[3][0] - element_coordinates[0][0];
const double J_10 = element_coordinates[1][1] - element_coordinates[0][1];
const double J_11 = element_coordinates[2][1] - element_coordinates[0][1];
const double J_12 = element_coordinates[3][1] - element_coordinates[0][1];
const double J_20 = element_coordinates[1][2] - element_coordinates[0][2];
const double J_21 = element_coordinates[2][2] - element_coordinates[0][2];
const double J_22 = element_coordinates[3][2] - element_coordinates[0][2];
  
// Compute sub determinants
const double d00 = J_11*J_22 - J_12*J_21;
const double d01 = J_12*J_20 - J_10*J_22;
const double d02 = J_10*J_21 - J_11*J_20;

const double d10 = J_02*J_21 - J_01*J_22;
const double d11 = J_00*J_22 - J_02*J_20;
const double d12 = J_01*J_20 - J_00*J_21;

const double d20 = J_01*J_12 - J_02*J_11;
const double d21 = J_02*J_10 - J_00*J_12;
const double d22 = J_00*J_11 - J_01*J_10;
  
// Compute determinant of Jacobian
double detJ = J_00*d00 + J_10*d10 + J_20*d20;

// Compute constants
const double C0 = element_coordinates[3][0] + element_coordinates[2][0] \\
                + element_coordinates[1][0] - element_coordinates[0][0];
const double C1 = element_coordinates[3][1] + element_coordinates[2][1] \\
                + element_coordinates[1][1] - element_coordinates[0][1];
const double C2 = element_coordinates[3][2] + element_coordinates[2][2] \\
                + element_coordinates[1][2] - element_coordinates[0][2];

// Get coordinates and map to the reference (FIAT) element
double x = coordinates[0];
double y = coordinates[1];
double z = coordinates[2];

x = (2.0*d00*x + 2.0*d10*y + 2.0*d20*z - d00*C0 - d10*C1 - d20*C2) / detJ;
y = (2.0*d01*x + 2.0*d11*y + 2.0*d21*z - d01*C0 - d11*C1 - d21*C2) / detJ;
z = (2.0*d02*x + 2.0*d12*y + 2.0*d22*z - d02*C0 - d12*C1 - d22*C2) / detJ;"""

# Snippet to generate combinations of derivatives of order n
combinations_snippet = """\
// Declare pointer to two dimensional array that holds combinations of derivatives and initialise
unsigned int **%(combinations)s = new unsigned int *[%(num_derivatives)s];
    
for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(combinations)s[j] = new unsigned int [%(n)s];
  for (unsigned int k = 0; k < %(n)s; k++)
    %(combinations)s[j][k] = 0;
}
    
// Generate combinations of derivatives
for (unsigned int row = 1; row < %(num_derivatives)s; row++)
{
  for (unsigned int num = 0; num < row; num++)
  {
    for (unsigned int col = %(n)s-1; col+1 > 0; col--)
    {
      if (%(combinations)s[row][col] + 1 > %(shape-1)s)
        %(combinations)s[row][col] = 0;
      else
      {
        %(combinations)s[row][col] += 1;
        break;
      }
    }
  }
}"""

# Snippet to transform of derivatives of order n
transform1D_snippet = """\
// Compute inverse of Jacobian
const double %(Jinv)s[1][1] =  {{1.0 / J_00}};

// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%(transform)s = new double *[%(num_derivatives)s];
    
for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(transform)s[j] = new double [%(num_derivatives)s];
  for (unsigned int k = 0; k < %(num_derivatives)s; k++)
    %(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(num_derivatives)s; col++)
  {
    for (unsigned int k = 0; k < %(n)s; k++)
      %(transform)s[row][col] *= %(Jinv)s[%(combinations)s[col][k]][%(combinations)s[row][k]];
  }
}"""

# Snippet to transform of derivatives of order n
transform2D_snippet = """\
// Compute inverse of Jacobian
const double %(Jinv)s[2][2] =  {{J_11 / detJ, -J_01 / detJ}, {-J_10 / detJ, J_00 / detJ}};

// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%(transform)s = new double *[%(num_derivatives)s];
    
for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(transform)s[j] = new double [%(num_derivatives)s];
  for (unsigned int k = 0; k < %(num_derivatives)s; k++)
    %(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(num_derivatives)s; col++)
  {
    for (unsigned int k = 0; k < %(n)s; k++)
      %(transform)s[row][col] *= %(Jinv)s[%(combinations)s[col][k]][%(combinations)s[row][k]];
  }
}"""

transform3D_snippet = """\
// Compute inverse of Jacobian
const double %(Jinv)s[3][3] =\
{{d00 / detJ, d10 / detJ, d20 / detJ},\
 {d01 / detJ, d11 / detJ, d21 / detJ},\
 {d02 / detJ, d12 / detJ, d22 / detJ}};

// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%(transform)s = new double *[%(num_derivatives)s];
    
for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(transform)s[j] = new double [%(num_derivatives)s];
  for (unsigned int k = 0; k < %(num_derivatives)s; k++)
    %(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(num_derivatives)s; col++)
  {
    for (unsigned int k = 0; k < %(n)s; k++)
      %(transform)s[row][col] *= %(Jinv)s[%(combinations)s[col][k]][%(combinations)s[row][k]];
  }
}"""

# Snippet to transform of derivatives of order n
transform2D_FIAT_snippet = """\
// Compute inverse of Jacobian, components are scaled because of difference in FFC/FIAT reference elements
const double %(Jinv)s[2][2] =  {{2*J_11 / detJ, -2*J_01 / detJ}, {-2*J_10 / detJ, 2*J_00 / detJ}};

// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%(transform)s = new double *[%(num_derivatives)s];
    
for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(transform)s[j] = new double [%(num_derivatives)s];
  for (unsigned int k = 0; k < %(num_derivatives)s; k++)
    %(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(num_derivatives)s; col++)
  {
    for (unsigned int k = 0; k < %(n)s; k++)
      %(transform)s[row][col] *= %(Jinv)s[%(combinations)s[col][k]][%(combinations)s[row][k]];
  }
}"""

transform3D_FIAT_snippet = """\
// Compute inverse of Jacobian, components are scaled because of difference in FFC/FIAT reference elements
const double %(Jinv)s[3][3] =\
{{2*d00 / detJ, 2*d10 / detJ, 2*d20 / detJ},\
 {2*d01 / detJ, 2*d11 / detJ, 2*d21 / detJ},\
 {2*d02 / detJ, 2*d12 / detJ, 2*d22 / detJ}};

// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%(transform)s = new double *[%(num_derivatives)s];
    
for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(transform)s[j] = new double [%(num_derivatives)s];
  for (unsigned int k = 0; k < %(num_derivatives)s; k++)
    %(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(num_derivatives)s; col++)
  {
    for (unsigned int k = 0; k < %(n)s; k++)
      %(transform)s[row][col] *= %(Jinv)s[%(combinations)s[col][k]][%(combinations)s[row][k]];
  }
}"""

# Code snippet for computing the inverse of the Jacobian and determinant in 2D
inverse_jacobian_2D = """\
// Compute determinant of Jacobian
double detJ%(restriction)s = J%(restriction)s_00*J%(restriction)s_11 - J%(restriction)s_01*J%(restriction)s_10;
  
// Compute inverse of Jacobian
const double Jinv%(restriction)s_00 =  J%(restriction)s_11 / detJ%(restriction)s;
const double Jinv%(restriction)s_01 = -J%(restriction)s_01 / detJ%(restriction)s;
const double Jinv%(restriction)s_10 = -J%(restriction)s_10 / detJ%(restriction)s;
const double Jinv%(restriction)s_11 =  J%(restriction)s_00 / detJ%(restriction)s;"""

# Code snippet for computing the inverse of the Jacobian and determinant in 3D
inverse_jacobian_3D = """\
// Compute sub determinants
const double d00 = J%(restriction)s_11*J%(restriction)s_22 - J%(restriction)s_12*J%(restriction)s_21;
const double d01 = J%(restriction)s_12*J%(restriction)s_20 - J%(restriction)s_10*J%(restriction)s_22;
const double d02 = J%(restriction)s_10*J%(restriction)s_21 - J%(restriction)s_11*J%(restriction)s_20;

const double d10 = J%(restriction)s_02*J%(restriction)s_21 - J%(restriction)s_01*J%(restriction)s_22;
const double d11 = J%(restriction)s_00*J%(restriction)s_22 - J%(restriction)s_02*J%(restriction)s_20;
const double d12 = J%(restriction)s_01*J%(restriction)s_20 - J%(restriction)s_00*J%(restriction)s_21;

const double d20 = J%(restriction)s_01*J%(restriction)s_12 - J%(restriction)s_02*J%(restriction)s_11;
const double d21 = J%(restriction)s_02*J%(restriction)s_10 - J%(restriction)s_00*J%(restriction)s_12;
const double d22 = J%(restriction)s_00*J%(restriction)s_11 - J%(restriction)s_01*J%(restriction)s_10;
  
// Compute determinant of Jacobian
double detJ%(restriction)s = J%(restriction)s_00*d00 + J%(restriction)s_10*d10 + J%(restriction)s_20*d20;
  
// Compute inverse of Jacobian
const double Jinv%(restriction)s_00 = d00 / detJ%(restriction)s;
const double Jinv%(restriction)s_01 = d10 / detJ%(restriction)s;
const double Jinv%(restriction)s_02 = d20 / detJ%(restriction)s;
const double Jinv%(restriction)s_10 = d01 / detJ%(restriction)s;
const double Jinv%(restriction)s_11 = d11 / detJ%(restriction)s;
const double Jinv%(restriction)s_12 = d21 / detJ%(restriction)s;
const double Jinv%(restriction)s_20 = d02 / detJ%(restriction)s;
const double Jinv%(restriction)s_21 = d12 / detJ%(restriction)s;
const double Jinv%(restriction)s_22 = d22 / detJ%(restriction)s;"""


# These are used with the "new" evaluate_dof.
map_onto_physical_1D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X[i][%(j)s][0];
const double w1 = X[i][%(j)s][0];

// Compute affine mapping y = F(X)
double y[1];
y[0] = w0*x[0][0] + w1*x[1][0];
"""
map_onto_physical_2D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X[i][%(j)s][0] - X[i][%(j)s][1];
const double w1 = X[i][%(j)s][0];
const double w2 = X[i][%(j)s][1];

// Compute affine mapping y = F(X)
double y[2];
y[0] = w0*x[0][0] + w1*x[1][0] + w2*x[2][0];
y[1] = w0*x[0][1] + w1*x[1][1] + w2*x[2][1];
"""
map_onto_physical_3D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X[i][%(j)s][0] - X[i][%(j)s][1] - X[i][%(j)s][2];
const double w1 = X[i][%(j)s][0];
const double w2 = X[i][%(j)s][1];
const double w3 = X[i][%(j)s][2];

// Compute affine mapping y = F(X)
double y[3];
y[0] = w0*x[0][0] + w1*x[1][0] + w2*x[2][0] + w3*x[3][0];
y[1] = w0*x[0][1] + w1*x[1][1] + w2*x[2][1] + w3*x[3][1];
y[2] = w0*x[0][2] + w1*x[1][2] + w2*x[2][2] + w3*x[3][2];
"""

calculate_dof = """\
// Take directional components
for(int k = 0; k < %(dim)d; k++)
  result += values[k]*D[i][%(index)s][k];
// Multiply by weights 
result *= W[i][%(index)s];"""


# Aug 26th 2008: These are used in the code generation for evaluate_dof:
# Code snippets for computing the Jacobian only
only_jacobian_1D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];"""

only_jacobian_2D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];"""

only_jacobian_3D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_02 = x%(restriction)s[3][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];
const double J%(restriction)s_12 = x%(restriction)s[3][1] - x%(restriction)s[0][1];
const double J%(restriction)s_20 = x%(restriction)s[1][2] - x%(restriction)s[0][2];
const double J%(restriction)s_21 = x%(restriction)s[2][2] - x%(restriction)s[0][2];
const double J%(restriction)s_22 = x%(restriction)s[3][2] - x%(restriction)s[0][2];"""

# UFC snippets, must be updated according to UFC. Latest update 2009-02-27
# Test snippets from UFC
cell_integral_call =\
"""%(reset_tensor)s

tabulate_tensor_tensor(A, w, c);
tabulate_tensor_quadrature(A, w, c);"""

exterior_facet_integral_call =\
"""%(reset_tensor)s

tabulate_tensor_tensor(A, w, c, facet);
tabulate_tensor_quadrature(A, w, c, facet);"""

interior_facet_integral_call =\
"""%(reset_tensor)s

tabulate_tensor_tensor(A, w, c0, c1, facet0, facet1);
tabulate_tensor_quadrature(A, w, c0, c1, facet0, facet1);"""

private_declarations = \
{"cell_integral_combined":\
"""
/// Tabulate the tensor for the contribution from a local cell
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c) const
{
%(tabulate_tensor)s
}
""",
"cell_integral_header":\
"""
/// Tabulate the tensor for the contribution from a local cell
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c) const;
""",
"cell_integral_implementation":\
"""
/// Tabulate the tensor for the contribution from a local cell
void %(classname)s::%(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c) const
{
%(tabulate_tensor)s
}
""",
"exterior_facet_integral_combined":\
"""
/// Tabulate the tensor for the contribution from a local exterior facet
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c,
                               unsigned int facet) const
{
%(tabulate_tensor)s
}
""",
"exterior_facet_integral_header":\
"""
/// Tabulate the tensor for the contribution from a local exterior facet
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c,
                               unsigned int facet) const;
""",
"exterior_facet_integral_implementation":\
"""
/// Tabulate the tensor for the contribution from a local exterior facet
void %(classname)s::%(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c,
                               unsigned int facet) const
{
%(tabulate_tensor)s
}
""",
"interior_facet_integral_combined":\
"""
/// Tabulate the tensor for the contribution from a local interior facet
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c0,
                               const ufc::cell& c1,
                               unsigned int facet0,
                               unsigned int facet1) const
{
%(tabulate_tensor)s
}
""",
"interior_facet_integral_header":\
"""
/// Tabulate the tensor for the contribution from a local interior facet
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c0,
                               const ufc::cell& c1,
                               unsigned int facet0,
                               unsigned int facet1) const;
""",
"interior_facet_integral_implementation":\
"""
/// Tabulate the tensor for the contribution from a local interior facet
void %(classname)s::%(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c0,
                               const ufc::cell& c1,
                               unsigned int facet0,
                               unsigned int facet1) const
{
%(tabulate_tensor)s
}
"""}

