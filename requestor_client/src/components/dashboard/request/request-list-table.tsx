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
import type { Request } from '../../../types/request';
import { getInitials } from '../../../utils/get-initials';
import { Scrollbar } from '../../scrollbar';

interface RequestsListTableProps {
  requests: Request[];
  requestsCount: number;
  onPageChange: (event: MouseEvent<HTMLButtonElement> | null, newPage: number) => void;
  onRowsPerPageChange?: (event: ChangeEvent<HTMLInputElement>) => void;
  page: number;
  rowsPerPage: number;
}

export const RequestListTable: FC<RequestsListTableProps> = (props) => {
  const {
    requests,
    requestsCount,
    onPageChange,
    onRowsPerPageChange,
    page,
    rowsPerPage,
    ...other
  } = props;
  const [selectedrequests, setSelectedrequests] = useState<string[]>([]);

  // Reset selected requests when requests change
  useEffect(
    () => {
      if (selectedrequests.length) {
        setSelectedrequests([]);
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [requests]
  );

  const handleSelectAllrequests = (event: ChangeEvent<HTMLInputElement>): void => {
    setSelectedrequests(
      event.target.checked
        ? requests.map((request) => request.workload_id)
        : []
    );
  };

  const handleSelectOneRequest = (
    event: ChangeEvent<HTMLInputElement>,
    requestId: string
  ): void => {
    if (!selectedrequests.includes(requestId)) {
      setSelectedrequests((prevSelected) => [...prevSelected, requestId]);
    } else {
      setSelectedrequests((prevSelected) => prevSelected.filter((id) => id !== requestId));
    }
  };

  const enableBulkActions = selectedrequests.length > 0;
  const selectedSomerequests = selectedrequests.length > 0
    && selectedrequests.length < requests.length;
  const selectedAllrequests = selectedrequests.length === requests.length;

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
          checked={selectedAllrequests}
          indeterminate={selectedSomerequests}
          onChange={handleSelectAllrequests}
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
                  checked={selectedAllrequests}
                  indeterminate={selectedSomerequests}
                  onChange={handleSelectAllrequests}
                />
              </TableCell>
              <TableCell>
                Name
              </TableCell>
              <TableCell>
                Machine Type
              </TableCell>
              <TableCell>
                Image
              </TableCell>
              <TableCell>
                Status
              </TableCell>
              <TableCell align="right">
                Actions
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {requests.map((request) => {
              const isrequestselected = selectedrequests.includes(request.workload_id);

              return (
                <TableRow
                  hover
                  key={request.workload_id}
                  selected={isrequestselected}
                >
                  <TableCell padding="checkbox">
                    <Checkbox
                      checked={isrequestselected}
                      onChange={(event) => handleSelectOneRequest(
                        event,
                        request.workload_id
                      )}
                      value={isrequestselected}
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
                          href={`/dashboard/requests/${request.workload_id}`}
                          passHref
                        >
                          <Link
                            color="inherit"
                            variant="subtitle2"
                          >
                            {request.workload_id}
                          </Link>
                        </NextLink>
                        <Typography
                          color="textSecondary"
                          variant="body2"
                        >
                          {request.workload_name}
                        </Typography>
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell>
                    {request.machine_type}
                  </TableCell>
                  <TableCell>
                    {request.machine_image}
                  </TableCell>
                  <TableCell>
                    <Typography
                      color="success.main"
                      variant="subtitle2"
                    >
                      {request.status}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    <NextLink
                      href={`/dashboard/requests/${request.workload_id}`} 
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
        count={requestsCount}
        onPageChange={onPageChange}
        onRowsPerPageChange={onRowsPerPageChange}
        page={page}
        rowsPerPage={rowsPerPage}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </div>
  );
};

RequestListTable.propTypes = {
  requests: PropTypes.array.isRequired,
  requestsCount: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired,
  onRowsPerPageChange: PropTypes.func,
  page: PropTypes.number.isRequired,
  rowsPerPage: PropTypes.number.isRequired
};
