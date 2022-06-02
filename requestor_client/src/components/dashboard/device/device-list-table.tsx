import { useEffect, useState } from 'react';
import type { ChangeEvent, FC, MouseEvent } from 'react';
import NextLink from 'next/link';
import numeral from 'numeral';
import PropTypes from 'prop-types';
import {
  Avatar,
  Box,
  Button,
  Checkbox,
  IconButton,
  Link,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TablePagination,
  TableRow,
  Typography
} from '@mui/material';
import { ArrowRight as ArrowRightIcon } from '../../../icons/arrow-right';
import { PencilAlt as PencilAltIcon } from '../../../icons/pencil-alt';
import type { Device } from '../../../types/device';
import { getInitials } from '../../../utils/get-initials';
import { Scrollbar } from '../../scrollbar';

interface DevicesListTableProps {
  devices: Device[];
  devicesCount: number;
  onPageChange: (event: MouseEvent<HTMLButtonElement> | null, newPage: number) => void;
  onRowsPerPageChange?: (event: ChangeEvent<HTMLInputElement>) => void;
  page: number;
  rowsPerPage: number;
}

export const DeviceListTable: FC<DevicesListTableProps> = (props) => {
  const {
    devices,
    devicesCount,
    onPageChange,
    onRowsPerPageChange,
    page,
    rowsPerPage,
    ...other
  } = props;
  const [selecteddevices, setSelecteddevices] = useState<string[]>([]);

  // Reset selected devices when devices change
  useEffect(
    () => {
      if (selecteddevices.length) {
        setSelecteddevices([]);
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [devices]
  );

  const handleSelectAlldevices = (event: ChangeEvent<HTMLInputElement>): void => {
    setSelecteddevices(
      event.target.checked
        ? devices.map((device) => device.id)
        : []
    );
  };

  const handleSelectOneDevice = (
    event: ChangeEvent<HTMLInputElement>,
    deviceId: string
  ): void => {
    if (!selecteddevices.includes(deviceId)) {
      setSelecteddevices((prevSelected) => [...prevSelected, deviceId]);
    } else {
      setSelecteddevices((prevSelected) => prevSelected.filter((id) => id !== deviceId));
    }
  };

  const enableBulkActions = selecteddevices.length > 0;
  const selectedSomedevices = selecteddevices.length > 0
    && selecteddevices.length < devices.length;
  const selectedAlldevices = selecteddevices.length === devices.length;

  return (
    <div {...other}>
      <Box
        sx={{
          backgroundColor: (theme) => theme.palette.mode === 'dark'
            ? 'neutral.800'
            : 'neutral.100',
          display: enableBulkActions ? 'block' : 'none',
          px: 2,
          py: 0.5
        }}
      >
        <Checkbox
          checked={selectedAlldevices}
          indeterminate={selectedSomedevices}
          onChange={handleSelectAlldevices}
        />
        <Button
          size="small"
          sx={{ ml: 2 }}
        >
          Delete
        </Button>
        <Button
          size="small"
          sx={{ ml: 2 }}
        >
          Edit
        </Button>
      </Box>
      <Scrollbar>
        <Table sx={{ minWidth: 700 }}>
          <TableHead sx={{ visibility: enableBulkActions ? 'collapse' : 'visible' }}>
            <TableRow>
              <TableCell padding="checkbox">
                <Checkbox
                  checked={selectedAlldevices}
                  indeterminate={selectedSomedevices}
                  onChange={handleSelectAlldevices}
                />
              </TableCell>
              <TableCell>
                Device ID
              </TableCell>
              <TableCell>
                Machine Type
              </TableCell>
              <TableCell>
                Uptime
              </TableCell>
              <TableCell align="right">
                Actions
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {devices.map((device) => {
              const isdeviceselected = selecteddevices.includes(device.id);

              return (
                <TableRow
                  hover
                  key={device.id}
                  selected={isdeviceselected}
                >
                  <TableCell padding="checkbox">
                    <Checkbox
                      checked={isdeviceselected}
                      onChange={(event) => handleSelectOneDevice(
                        event,
                        device.id
                      )}
                      value={isdeviceselected}
                    />
                  </TableCell>
                  <TableCell>
                    <Box
                      sx={{
                        alignItems: 'center',
                        display: 'flex'
                      }}
                    >
                      

                      <Box sx={{ ml: 1 }}>
                        <NextLink
                          href={`/dashboard/devices/${device.id}`}
                          passHref
                        >
                          <Link
                            color="inherit"
                            variant="subtitle2"
                          >
                            {device.id}
                          </Link>
                        </NextLink>
                        <Typography
                          color="textSecondary"
                          variant="body2"
                        >
                          {device.name}
                        </Typography>
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell>
                    {device.machineType}
                  </TableCell>
                  <TableCell>
                    <Typography
                      color="success.main"
                      variant="subtitle2"
                    >
                      {device.uptime}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    <NextLink
                      href={`/dashboard/devices/${device.id}`} 
                      passHref
                    >
                      <IconButton component="a">
                        <ArrowRightIcon fontSize="small" />
                      </IconButton>
                    </NextLink>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </Scrollbar>
      <TablePagination
        component="div"
        count={devicesCount}
        onPageChange={onPageChange}
        onRowsPerPageChange={onRowsPerPageChange}
        page={page}
        rowsPerPage={rowsPerPage}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </div>
  );
};

DeviceListTable.propTypes = {
  devices: PropTypes.array.isRequired,
  devicesCount: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired,
  onRowsPerPageChange: PropTypes.func,
  page: PropTypes.number.isRequired,
  rowsPerPage: PropTypes.number.isRequired
};
