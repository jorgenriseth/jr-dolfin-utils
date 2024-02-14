import dolfin as df


class Domain(df.Mesh):
    def __init__(
        self,
        mesh: df.Mesh,
        subdomains: df.MeshFunction,
        boundaries: df.MeshFunction,
        **kwargs
    ):
        super().__init__(mesh, **kwargs)
        self.subdomains = transfer_meshfunction(self, subdomains)
        self.boundaries = transfer_meshfunction(self, boundaries)


def transfer_meshfunction(
    newmesh: df.Mesh, meshfunc: df.MeshFunction
) -> df.MeshFunction:
    newtags = df.MeshFunction("size_t", newmesh, dim=meshfunc.dim())  # type: ignore
    newtags.set_values(meshfunc)  # type: ignore
    return newtags


class MMSInterval(Domain):
    def __init__(self, N: int):
        subdomains = {
            2: df.CompiledSubDomain("abs(x[0]) <= 0.8 + tol", tol=df.DOLFIN_EPS),
            1: df.CompiledSubDomain("abs(x[0]) >= 0.8 - tol", tol=df.DOLFIN_EPS),
        }
        subboundaries = {
            1: df.CompiledSubDomain("near(x[0], -1) && on_boundary"),
            2: df.CompiledSubDomain("near(x[0], 1) && on_boundary"),
        }
        normals = {1: -1.0, 2: 1.0}

        mesh = df.IntervalMesh(N, -1.0, 1.0)
        subdomain_tags = mark_subdomains(subdomains, mesh, 0, default_value=1)
        boundary_tags = mark_subdomains(subboundaries, mesh, 1)

        super().__init__(mesh, subdomain_tags, boundary_tags)
        self.normals = normals


class MMSDomain(Domain):
    def __init__(self, N: int):
        subdomains = {
            1: df.CompiledSubDomain("x[1] <= +tol", tol=DOLFIN_EPS),
            2: df.CompiledSubDomain("x[1] >= -tol", tol=DOLFIN_EPS),
        }
        subboundaries = {
            1: df.CompiledSubDomain("near(x[0], -1) && on_boundary"),
            2: df.CompiledSubDomain("near(x[0], 1) && on_boundary"),
            3: df.CompiledSubDomain("near(x[1], -1) && on_boundary"),
            4: df.CompiledSubDomain("near(x[1], 1) && on_boundary"),
        }
        normals = {
            1: np.array([-1.0, +0.0]),
            2: np.array([+1.0, +0.0]),
            3: np.array([+0.0, -1.0]),
            4: np.array([+0.0, +1.0]),
        }

        mesh = df.RectangleMesh(
            df.Point(-1, -1), df.Point(1, 1), N, N, diagonal="crossed"
        )
        subdomain_tags = mark_subdomains(subdomains, mesh, 0, default_value=1)
        boundary_tags = mark_subdomains(subboundaries, mesh, 1)

        super().__init__(mesh, subdomain_tags, boundary_tags)
        self.normals = normals


def mark_subdomains(
    subdomains: dict[int, df.CompiledSubDomain],
    mesh: df.Mesh,
    codim: int,
    default_value: int = 0,
):
    dim = mesh.topology().dim() - codim
    subdomain_tags = df.MeshFunction("size_t", mesh, dim=dim, value=default_value)
    for tag, subd in subdomains.items():
        subd.mark(subdomain_tags, tag)
    return subdomain_tags
