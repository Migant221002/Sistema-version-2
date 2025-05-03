import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  TablePagination,
  Box,
  CircularProgress,
  Button,
  Card,
  CardContent,
  TextField
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const PagoList = () => {
  const [pagos, setPagos] = useState([]);
  const [totalDia, setTotalDia] = useState(0);
  const [totalMes, setTotalMes] = useState(0);
  const [totalPorFecha, setTotalPorFecha] = useState(0);
  const [fechaSeleccionada, setFechaSeleccionada] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const navigate = useNavigate();

  useEffect(() => {
    fetchPagos();
  }, []);

  const fetchPagos = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://127.0.0.1:5000/api/pagos', {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      const pagosData = response.data.map(pago => ({
        ...pago,
        fecha_pago: new Date(pago.fecha_pago).toISOString().split("T")[0]
      }));

      setPagos(pagosData);

      const hoy = new Date().toISOString().split("T")[0];
      const fechaActual = new Date();
      const mesActual = fechaActual.getMonth() + 1;
      const anioActual = fechaActual.getFullYear();

      const totalDiaCalculado = pagosData.reduce((acc, pago) => {
        return pago.fecha_pago === hoy ? acc + Number(pago.total) : acc;
      }, 0);
      setTotalDia(totalDiaCalculado);

      const totalMesCalculado = pagosData.reduce((acc, pago) => {
        const fechaPago = new Date(pago.fecha_pago);
        return fechaPago.getMonth() + 1 === mesActual && fechaPago.getFullYear() === anioActual
          ? acc + Number(pago.total)
          : acc;
      }, 0);
      setTotalMes(totalMesCalculado);

      setLoading(false);
    } catch (error) {
      console.error('Error al cargar los pagos:', error);
      setError('Error al cargar la lista de pagos');
      setLoading(false);
    }
  };

  const handleFechaChange = (event) => {
    const fechaElegida = event.target.value;
    setFechaSeleccionada(fechaElegida);

    fetchPagos();

    const totalCalculado = pagos.reduce((acc, pago) => {
      return pago.fecha_pago === fechaElegida ? acc + Number(pago.total) : acc;
    }, 0);

    setTotalPorFecha(totalCalculado);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container>
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      </Container>
    );
  }

  return (
    <Container>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
          Lista de Pagos
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          onClick={() => navigate('/pagos/nuevo')}
          sx={{ mt: 4, mb: 2 }}
        >
          Nuevo Pago
        </Button>
      </Box>

      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <Card sx={{ minWidth: 250 }}>
          <CardContent>
            <Typography variant="h6">Total del Día</Typography>
            <Typography variant="h5" color="primary">Q{totalDia}</Typography>
          </CardContent>
        </Card>
        <Card sx={{ minWidth: 250 }}>
          <CardContent>
            <Typography variant="h6">Total del Mes</Typography>
            <Typography variant="h5" color="primary">Q{totalMes}</Typography>
          </CardContent>
        </Card>
      </Box>

      {/* Filtro de pagos por fecha con mejor diseño */}
      <Box sx={{ mb: 3, p: 2, borderRadius: 2, bgcolor: 'whitesmoke', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="h6" sx={{ mb: 1 }}>Selecciona una fecha para ver pagos:</Typography>
        <TextField
          type="date"
          variant="outlined"
          value={fechaSeleccionada}
          onChange={handleFechaChange}
          sx={{
            width: '50%',
            bgcolor: 'white',
            borderRadius: 1,
            boxShadow: 1
          }}
        />
        {fechaSeleccionada && (
          <Typography sx={{ mt: 2, fontSize: 18, fontWeight: 'bold', color: 'green' }}>
            Total pagado el {fechaSeleccionada}: <strong>Q{totalPorFecha}</strong>
          </Typography>
        )}
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Empleado</TableCell>
              <TableCell>Libras</TableCell>
              <TableCell>Precio por Libra</TableCell>
              <TableCell>Total</TableCell>
              <TableCell>Fecha de Pago</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {pagos
              .filter(pago => fechaSeleccionada ? pago.fecha_pago === fechaSeleccionada : true) // ✅ Filtrar la tabla
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((pago) => (
                <TableRow key={pago.id}>
                  <TableCell>{pago.id}</TableCell>
                  <TableCell>{pago.empleado ? `${pago.empleado.nombre} (${pago.empleado.dpi})` : 'N/A'}</TableCell>
                  <TableCell>{pago.libras}</TableCell>
                  <TableCell>Q{pago.precio_libra}</TableCell>
                  <TableCell>Q{pago.total}</TableCell>
                  <TableCell>{pago.fecha_pago}</TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={pagos.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={(event, newPage) => setPage(newPage)}
          onRowsPerPageChange={(event) => setRowsPerPage(parseInt(event.target.value, 10))}
          labelRowsPerPage="Filas por página"
        />
      </TableContainer>
    </Container>
  );
};

export default PagoList;