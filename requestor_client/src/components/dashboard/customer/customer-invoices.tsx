import { useState, useEffect, useCallback } from 'react';
import type { FC } from 'react';
import NextLink from 'next/link';
import { format } from 'date-fns';
import {
  Card,
  CardHeader,
  Divider,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TablePagination,
  TableRow
} from '@mui/material';
import { useMounted } from '../../../hooks/use-mounted';
import { ArrowRight as ArrowRightIcon } from '../../../icons/arrow-right';
import type { CustomerInvoice } from '../../../types/customer';
import { MoreMenu } from '../../more-menu';
import { Scrollbar } from '../../scrollbar';
import { SeverityPill } from '../../severity-pill';
import { requestApi } from 'src/__fake-api__/request-api';
import { RequestResponse } from 'src/types/request';
import { ArrowDownward } from '@mui/icons-material';

export const CustomerInvoices: FC = (props) => {

  const isMounted = useMounted();
  const [responses, setResponses] = useState<RequestResponse[]>([]);

  const getResults = useCallback(async (workload_id: string) => {
    try {
      const data = await requestApi.getResponses(workload_id);

      if (isMounted()) {
        setResponses(data);
      }
    } catch (err) {
      console.error(err);
    }
  }, [isMounted]);

  useEffect(() => {
    const path = window.location.pathname.split("/");
    getResults(path[path.length-1]);
  }, [getResults]);

  return (
    <Card {...props}>
      <CardHeader
        action={<MoreMenu />}
        title="Workload Results"
      />
      <Divider />
      <Scrollbar>
        <Table sx={{ minWidth: 600 }}>
          <TableHead>
            <TableRow>
              <TableCell>
                ID
              </TableCell>
              <TableCell>
                Artefact URL
              </TableCell>
              <TableCell>
                Duration
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
            {responses.map((response, index) => (
              <TableRow key={response.result_id}>
                <TableCell>
                  #
                  {index+1}
                </TableCell>
                <TableCell>
                  {response.file_url}
                </TableCell>
                <TableCell>
                  {response.time_consumed}
                </TableCell>
                <TableCell>
                  <SeverityPill color={response.status === 'success' ? 'success' : 'error'}>
                    {response.status}
                  </SeverityPill>
                </TableCell>
                <TableCell align="right">
                  <NextLink
                    href={response.file_url}
                    passHref
                  >
                    <IconButton component="a">
                      <ArrowDownward fontSize="small" />
                    </IconButton>
                  </NextLink>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Scrollbar>
      <TablePagination
        component="div"
        count={responses.length}
        onPageChange={(): void => {
        }}
        onRowsPerPageChange={(): void => {
        }}
        page={0}
        rowsPerPage={5}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </Card>
  );
};
